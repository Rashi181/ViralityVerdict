from datetime import datetime
from typing import Literal
from pydantic import BaseModel

class VideoJobResponse(BaseModel):
    id: str; status: Literal["queued", "processing", "completed", "failed", "cancelled"]; filename: str; content_type: str; size_bytes: int; created_at: datetime; error: str | None; limitations: list[str]; duration_seconds: float | None = None; width: int | None = None; height: int | None = None
