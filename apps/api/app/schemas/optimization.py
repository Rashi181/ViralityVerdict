from typing import Literal
from pydantic import BaseModel, Field

CaptionStyle = Literal["formal", "sarcastic", "humorous-tech", "humorous-non-tech"]

class OptimizationRequest(BaseModel):
    draft_text: str = Field(min_length=1, max_length=2200)
    call_to_action: str = Field(min_length=1, max_length=240)

class CaptionVariant(BaseModel): style: CaptionStyle; text: str
class OptimizationResponse(BaseModel):
    source_tier: Literal["user_supplied"]
    captions: list[CaptionVariant]
    suggestions: list[str]
    persona_reactions: list[str]
    limitations: list[str]
