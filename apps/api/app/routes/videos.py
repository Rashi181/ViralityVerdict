import shutil
import json
import subprocess
from pathlib import Path
from tempfile import gettempdir
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from app.repositories.videos import VideoRepository
from app.routes.auth import current_user
from app.schemas.videos import VideoJobResponse

router=APIRouter(); MAX_SIZE=25*1024*1024; ALLOWED={"video/mp4":b"ftyp", "video/webm":b"\x1aE\xdf\xa3"}; STORE=Path(gettempdir())/"verdict-private-uploads"
def repository(request: Request) -> VideoRepository: return request.app.state.video_repository
def response(x: dict) -> VideoJobResponse: return VideoJobResponse(id=x["_id"],status=x["status"],filename=x["filename"],content_type=x["content_type"],size_bytes=x["size_bytes"],created_at=x["created_at"],error=x.get("error"),limitations=x["limitations"],duration_seconds=x.get("duration_seconds"),width=x.get("width"),height=x.get("height"))

@router.post("/videos",response_model=VideoJobResponse,status_code=status.HTTP_201_CREATED)
async def upload_video(file: UploadFile=File(...), user:dict=Depends(current_user), repo:VideoRepository=Depends(repository))->VideoJobResponse:
    if file.content_type not in ALLOWED: raise HTTPException(422,"Only MP4 or WebM video uploads are accepted")
    data=await file.read(MAX_SIZE+1)
    if len(data)>MAX_SIZE: raise HTTPException(422,"Video exceeds the 25 MB local-development limit")
    if ALLOWED[file.content_type] not in data[:32]: raise HTTPException(422,"File signature does not match the declared video type")
    STORE.mkdir(parents=True,exist_ok=True)
    private_path=STORE/f"upload-{Path(file.filename or 'draft-video').name}"
    private_path.write_bytes(data)
    result=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration:stream=width,height","-of","json",str(private_path)],capture_output=True,text=True,timeout=10)
    try:
        probe=json.loads(result.stdout); stream=next(item for item in probe.get("streams",[]) if "width" in item); metadata={"duration_seconds":round(float(probe["format"]["duration"]),2),"width":stream["width"],"height":stream["height"]}; job_status="completed"; error=None
    except (KeyError, StopIteration, ValueError, json.JSONDecodeError):
        metadata={}; job_status="failed"; error="FFmpeg could not read this video; no analysis was produced."
    record=repo.create(user["_id"],{"status":job_status,"filename":Path(file.filename or "draft-video").name,"content_type":file.content_type,"size_bytes":len(data),"limitations":["Private local-development storage only; no public URL is created.","Only FFmpeg metadata extraction completed. Scene extraction, transcript, OCR, and AI analysis are unavailable."],"error":error,**metadata})
    return response(record)

@router.get("/videos",response_model=list[VideoJobResponse])
def list_videos(user:dict=Depends(current_user),repo:VideoRepository=Depends(repository))->list[VideoJobResponse]: return [response(x) for x in repo.list_for_owner(user["_id"])]
