import json
import subprocess
from pathlib import Path
from tempfile import gettempdir
from uuid import uuid4
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from app.repositories.videos import VideoRepository
from app.routes.auth import current_user
from app.integrations.gemini_reel import GeminiReelAnalysis, GeminiUnavailableError, ReelAnalyzer
from app.schemas.videos import AnalysisEvidence, ReelFinding, ReelReadinessResponse, VideoJobResponse

router=APIRouter(); MAX_SIZE=25*1024*1024; ALLOWED={"video/mp4":b"ftyp", "video/webm":b"\x1aE\xdf\xa3"}; STORE=Path(gettempdir())/"verdict-private-uploads"
def repository(request: Request) -> VideoRepository: return request.app.state.video_repository
def analyzer(request: Request) -> ReelAnalyzer: return request.app.state.reel_analyzer
def response(x: dict) -> VideoJobResponse: return VideoJobResponse(id=x["_id"],status=x["status"],filename=x["filename"],content_type=x["content_type"],size_bytes=x["size_bytes"],created_at=x["created_at"],error=x.get("error"),limitations=x["limitations"],duration_seconds=x.get("duration_seconds"),width=x.get("width"),height=x.get("height"))


def extract_private_frames(private_path: Path) -> tuple[int, str, list[str]]:
    frame_directory = STORE / f"frames-{uuid4()}"
    frame_directory.mkdir(parents=True, exist_ok=True)
    commands = [
        # The opening gets denser coverage because it carries most hook evidence.
        (["ffmpeg", "-v", "error", "-t", "5", "-i", str(private_path), "-vf", "fps=2", "-frames:v", "10", str(frame_directory / "hook-%03d.jpg")], "opening: every 0.5 seconds for the first 5 seconds"),
        # Regular coverage avoids sending hundreds of nearly identical frames to a later model.
        (["ffmpeg", "-v", "error", "-ss", "5", "-i", str(private_path), "-vf", "fps=1/3", "-frames:v", "20", str(frame_directory / "regular-%03d.jpg")], "body: every 3 seconds after the opening"),
        # Scene detection adds visual transitions that timing-only sampling can miss.
        (["ffmpeg", "-v", "error", "-i", str(private_path), "-vf", "select=gt(scene\\,0.30)", "-fps_mode", "vfr", "-frames:v", "12", str(frame_directory / "scene-%03d.jpg")], "scene changes: up to 12 additional frames when FFmpeg detects a material visual change"),
    ]
    for command, _ in commands:
        subprocess.run(command, capture_output=True, text=True, timeout=20, check=False)
    frame_count = len(list(frame_directory.glob("*.jpg")))
    strategy = "; ".join(description for _, description in commands)
    hooks = sorted(frame_directory.glob("hook-*.jpg"))
    scenes = sorted(frame_directory.glob("scene-*.jpg"))
    regular = sorted(frame_directory.glob("regular-*.jpg"))
    strategic = [*hooks[:1], *hooks[-1:], *(scenes[:1] or regular[:1])]
    unique = list(dict.fromkeys(str(path) for path in strategic))
    return frame_count, strategy, unique

@router.post("/videos",response_model=VideoJobResponse,status_code=status.HTTP_201_CREATED)
async def upload_video(file: UploadFile=File(...), user:dict=Depends(current_user), repo:VideoRepository=Depends(repository))->VideoJobResponse:
    if file.content_type not in ALLOWED: raise HTTPException(422,"Only MP4 or WebM video uploads are accepted")
    data=await file.read(MAX_SIZE+1)
    if len(data)>MAX_SIZE: raise HTTPException(422,"Video exceeds the 25 MB local-development limit")
    if ALLOWED[file.content_type] not in data[:32]: raise HTTPException(422,"File signature does not match the declared video type")
    STORE.mkdir(parents=True,exist_ok=True)
    private_path=STORE/f"upload-{uuid4()}-{Path(file.filename or 'draft-video').name}"
    private_path.write_bytes(data)
    result=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration:stream=width,height","-of","json",str(private_path)],capture_output=True,text=True,timeout=10)
    try:
        probe=json.loads(result.stdout); stream=next(item for item in probe.get("streams",[]) if "width" in item); frame_count, strategy, strategic_frame_paths = extract_private_frames(private_path); metadata={"duration_seconds":round(float(probe["format"]["duration"]),2),"width":stream["width"],"height":stream["height"],"sampled_frame_count":frame_count,"sampling_strategy":strategy,"strategic_frame_paths":strategic_frame_paths}; job_status="completed"; error=None
    except (KeyError, StopIteration, ValueError, json.JSONDecodeError):
        metadata={}; job_status="failed"; error="FFmpeg could not read this video; no analysis was produced."
    record=repo.create(user["_id"],{"status":job_status,"filename":Path(file.filename or "draft-video").name,"content_type":file.content_type,"size_bytes":len(data),"private_path":str(private_path),"limitations":["Private local-development storage only; no public URL is created.","Provider analysis is not run until you explicitly request it."],"error":error,**metadata})
    return response(record)

@router.get("/videos",response_model=list[VideoJobResponse])
def list_videos(user:dict=Depends(current_user),repo:VideoRepository=Depends(repository))->list[VideoJobResponse]: return [response(x) for x in repo.list_for_owner(user["_id"])]


@router.get("/videos/{video_id}/analysis", response_model=ReelReadinessResponse)
def reel_readiness(video_id: str, user: dict = Depends(current_user), repo: VideoRepository = Depends(repository)) -> ReelReadinessResponse:
    video = repo.find_for_owner(user["_id"], video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="Private video job not found")
    if video["status"] != "completed":
        return ReelReadinessResponse(status="unavailable", label="Analysis unavailable", evidence=[], findings=[], attention_risks=[], persona_reactions=[], cumulative_recommendation="Fix the private upload job before requesting analysis.", limitations=[video.get("error") or "Video processing did not complete."])
    evidence = [
        AnalysisEvidence(duration_seconds=video["duration_seconds"], width=video["width"], height=video["height"], sampled_frame_count=0, sample_interval_seconds=0, sampling_strategy="FFmpeg metadata probe", source="ffmpeg_metadata"),
        AnalysisEvidence(duration_seconds=video["duration_seconds"], width=video["width"], height=video["height"], sampled_frame_count=video.get("sampled_frame_count", 0), sample_interval_seconds=0, sampling_strategy=video.get("sampling_strategy", "No frame-sampling strategy was recorded."), source="ffmpeg_frame_sampling"),
    ]
    saved = video.get("gemini_analysis")
    if saved:
        provider = saved.get("provider", "model")
        return ReelReadinessResponse(status="ready", score=None, label=f"{provider.title()} analysis ready", evidence=evidence, findings=[ReelFinding.model_validate(item) for item in saved["findings"]], attention_risks=[], persona_reactions=[], cumulative_recommendation=saved["summary"], limitations=saved["limitations"] + [f"Timestamped findings are {provider} hypotheses based on this private draft, not actual viewer-retention data.", "No persona reactions are shown unless Verdict has current, authorized aggregate audience evidence."])
    return ReelReadinessResponse(status="awaiting_ai_analysis", score=None, label="Ready for strategic analysis", evidence=evidence, findings=[], attention_risks=[], persona_reactions=[], cumulative_recommendation="Your private upload is ready. Select Analyze strategic frames to request evidence-limited hook, scene-change, pacing, clarity, CTA, and accessibility feedback.", limitations=["No provider is called until you explicitly select Analyze strategic frames.", "No Reel Readiness score, retention curve, or persona reaction is shown before evidence-grounded analysis exists."])


@router.post("/videos/{video_id}/analysis", response_model=ReelReadinessResponse)
def analyze_reel(video_id: str, request: Request, user: dict = Depends(current_user), repo: VideoRepository = Depends(repository), reel_analyzer: ReelAnalyzer = Depends(analyzer)) -> ReelReadinessResponse:
    video = repo.find_for_owner(user["_id"], video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="Private video job not found")
    if video["status"] != "completed":
        raise HTTPException(status_code=409, detail="This private draft did not complete local processing.")
    path = Path(video.get("private_path", ""))
    if not path.is_file():
        raise HTTPException(status_code=409, detail="The local private draft is no longer available. Upload it again before analysis.")
    try:
        result: GeminiReelAnalysis = reel_analyzer.analyze(path, content_type=video["content_type"], duration_seconds=video["duration_seconds"], frame_paths=[Path(item) for item in video.get("strategic_frame_paths", [])])
    except GeminiUnavailableError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    repo.update_for_owner(user["_id"], video_id, {"gemini_analysis": {**result.model_dump(mode="json"), "provider": request.app.state.reel_analysis_provider}})
    return reel_readiness(video_id, user, repo)
