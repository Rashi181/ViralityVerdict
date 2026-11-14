from datetime import datetime
from typing import Literal
from pydantic import BaseModel

class VideoJobResponse(BaseModel):
    id: str; status: Literal["queued", "processing", "completed", "failed", "cancelled"]; filename: str; content_type: str; size_bytes: int; created_at: datetime; error: str | None; limitations: list[str]; duration_seconds: float | None = None; width: int | None = None; height: int | None = None


class AnalysisEvidence(BaseModel):
    duration_seconds: float
    width: int
    height: int
    sampled_frame_count: int
    sample_interval_seconds: float
    sampling_strategy: str
    source: Literal["ffmpeg_metadata", "ffmpeg_frame_sampling"]


class ReelReadinessResponse(BaseModel):
    status: Literal["awaiting_ai_analysis", "unavailable"]
    score: None = None
    label: str
    evidence: list[AnalysisEvidence]
    attention_risks: list[str]
    persona_reactions: list[str]
    cumulative_recommendation: str
    limitations: list[str]
