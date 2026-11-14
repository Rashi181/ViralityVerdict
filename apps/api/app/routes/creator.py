import re
from collections import Counter
from datetime import datetime

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from app.routes.auth import current_user

router = APIRouter()


class CreatorSummary(BaseModel):
    sample_size: int
    date_start: datetime | None
    date_end: datetime | None
    total_views: int
    average_engagement_rate: float | None
    top_media_ids: list[str]
    recurring_formats: dict[str, int]
    observed_hashtags: list[str]
    observed_caption_keywords: list[str]
    hook_samples: list[str]
    limitations: list[str]


@router.get("/creator/profile", response_model=CreatorSummary)
def profile(request: Request, user: dict = Depends(current_user)) -> CreatorSummary:
    records = request.app.state.import_repository.list_for_owner(user["_id"])
    # Imports may be retried; each observed media ID is analyzed only once.
    by_media_id = {item["media_id"]: item for record in records for item in record["media"]}
    media = list(by_media_id.values())
    if not media:
        return CreatorSummary(
            sample_size=0, date_start=None, date_end=None, total_views=0,
            average_engagement_rate=None, top_media_ids=[], recurring_formats={},
            observed_hashtags=[], observed_caption_keywords=[], hook_samples=[],
            limitations=["No imported creator history is available."],
        )

    dates = [
        datetime.fromisoformat(item["published_at"].replace("Z", "+00:00"))
        if isinstance(item["published_at"], str) else item["published_at"]
        for item in media
    ]
    rates = [
        (item["likes"] + item["comments"]) / item["views"] * 100
        for item in media if item["views"]
    ]
    top = sorted(media, key=lambda item: item["views"], reverse=True)[:3]
    hashtags = Counter(
        tag.lower() for item in media
        for tag in re.findall(r"(?<!\w)#([\w]+)", item.get("caption", ""))
    )
    ignored_words = {"about", "after", "and", "from", "have", "into", "just", "later", "that", "the", "this", "three", "tips", "with", "your"}
    keywords = Counter(
        token.lower()
        for item in media
        for token in re.findall(r"\b[a-zA-Z][a-zA-Z0-9]{3,}\b", re.sub(r"(?<!\w)#[\w]+", "", item.get("caption", "")))
        if token.lower() not in ignored_words
    )
    hooks = [
        item["caption"].strip().splitlines()[0][:160]
        for item in top if item.get("caption", "").strip()
    ]
    limitations = ["Metrics are user-imported and not API-verified."]
    if len(media) < 5:
        limitations.append("Sparse history: comparisons are directional, not causal.")
    limitations.append(
        "Semantic topic and brand-voice classification is unavailable until an authorized model integration is configured."
    )
    return CreatorSummary(
        sample_size=len(media), date_start=min(dates), date_end=max(dates),
        total_views=sum(item["views"] for item in media),
        average_engagement_rate=round(sum(rates) / len(rates), 2) if rates else None,
        top_media_ids=[item["media_id"] for item in top],
        recurring_formats=dict(Counter(item["media_type"] for item in media)),
        observed_hashtags=[f"#{tag}" for tag, _ in hashtags.most_common(5)],
        observed_caption_keywords=[keyword for keyword, _ in keywords.most_common(8)],
        hook_samples=hooks, limitations=limitations,
    )
