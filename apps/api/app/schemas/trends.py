from datetime import datetime
from typing import Literal

from pydantic import AnyHttpUrl, BaseModel, Field


class TrendSourceInput(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    source_url: AnyHttpUrl
    observed_at: datetime
    niche_relevance: str = Field(min_length=1, max_length=300)
    geographic_relevance: str = Field(min_length=1, max_length=100)
    source_type: Literal["google_trends", "youtube", "other_documented_source"]


class TrendImportRequest(BaseModel):
    consent_confirmed: bool
    signals: list[TrendSourceInput] = Field(min_length=1, max_length=25)


class TrendSignal(TrendSourceInput):
    id: str
    retrieved_at: datetime
    freshness: Literal["current", "stale"]


class TrendFeedResponse(BaseModel):
    status: Literal["available", "unavailable"]
    signals: list[TrendSignal]
    fallback: str | None
    limitations: list[str]
