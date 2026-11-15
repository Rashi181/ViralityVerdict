from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


AudienceField = Literal["age_distribution", "gender_distribution", "top_locations", "follower_count", "other"]


class AudienceAggregate(BaseModel):
    field: AudienceField
    values: dict[str, str | int | float] = Field(min_length=1, max_length=50)
    source: Literal["user_import", "instagram_api", "synthetic_demo"]
    source_label: str = Field(min_length=1, max_length=160)
    as_of: datetime


class AudienceImportRequest(BaseModel):
    consent_confirmed: bool
    aggregates: list[AudienceAggregate] = Field(min_length=1, max_length=20)


class AudienceImportResponse(BaseModel):
    id: str
    aggregate_count: int
    created_at: datetime
    limitations: list[str]


class PersonaFeedbackRequest(BaseModel):
    note: str = Field(min_length=1, max_length=1000)


class AudiencePersonaResponse(BaseModel):
    id: str
    status: Literal["observed", "provisional", "synthetic_demo"]
    label: str
    intended_use: str
    observed_evidence: list[AudienceAggregate]
    inferred_interests: list[str]
    likely_motivations: list[str]
    content_preferences: list[str]
    suggested_hooks: list[str]
    pacing_considerations: list[str]
    cta_preferences: list[str]
    unknowns: list[str]
    confidence: Literal["low", "medium"]
    data_coverage: str
    freshness: datetime | None
    feedback_note: str | None
