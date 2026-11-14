from typing import Literal
from pydantic import BaseModel, Field

class OptimizationRequest(BaseModel):
    draft_text: str = Field(min_length=1, max_length=2200)
    call_to_action: str = Field(min_length=1, max_length=240)
    refinement_prompt: str | None = Field(default=None, max_length=300)

class CaptionRecommendation(BaseModel):
    id: Literal["concise", "context_first", "question_led"]
    text: str


class HashtagRecommendation(BaseModel):
    tag: str
    source: Literal["creator_provided_keyword"]
    explanation: str


class OptimizationResponse(BaseModel):
    source_tier: Literal["user_supplied"]
    captions: list[CaptionRecommendation]
    hashtags: list[HashtagRecommendation]
    suggestions: list[str]
    persona_reactions: list[str]
    limitations: list[str]
