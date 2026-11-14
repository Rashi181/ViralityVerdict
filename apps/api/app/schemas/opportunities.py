from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.services.scoring import ScoreInputs


class OpportunityRequest(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    angle: str = Field(min_length=1, max_length=600)
    hook: str = Field(min_length=1, max_length=300)
    format: Literal["reel", "post"]
    effort: Literal["low", "medium", "high"]
    evidence: list[str] = Field(min_length=1, max_length=10)
    score_inputs: ScoreInputs


class OpportunityResponse(OpportunityRequest):
    id: str
    score: float
    score_version: str
    confidence: Literal["standard", "reduced"]
    created_at: datetime
