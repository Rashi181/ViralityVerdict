from pydantic import BaseModel, Field


class ScoreInputs(BaseModel):
    audience_fit: float = Field(ge=0, le=100)
    trend_relevance: float = Field(ge=0, le=100)
    novelty: float = Field(ge=0, le=100)
    feasibility: float = Field(ge=0, le=100)
    missing_components: list[str] = []


def opportunity_score(inputs: ScoreInputs) -> float:
    return round(0.35 * inputs.audience_fit + 0.30 * inputs.trend_relevance + 0.20 * inputs.novelty + 0.15 * inputs.feasibility, 2)


def confidence(inputs: ScoreInputs) -> str:
    return "reduced" if inputs.missing_components else "standard"
