from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, Request, status

from app.repositories.trends import TrendRepository
from app.routes.auth import current_user
from app.schemas.trends import TrendFeedResponse, TrendImportRequest, TrendSignal

router = APIRouter()
FRESHNESS_WINDOW = timedelta(days=7)


def repository(request: Request) -> TrendRepository:
    return request.app.state.trend_repository


@router.post("/trends/import", response_model=list[TrendSignal], status_code=status.HTTP_201_CREATED)
def import_signals(payload: TrendImportRequest, user: dict = Depends(current_user), repo: TrendRepository = Depends(repository)) -> list[TrendSignal]:
    records = repo.create(user["_id"], [signal.model_dump(mode="json") for signal in payload.signals])
    return [as_signal(record) for record in records]


def as_signal(record: dict) -> TrendSignal:
    observed_at = record["observed_at"]
    if isinstance(observed_at, str):
        observed_at = datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
    freshness = "current" if datetime.now(UTC) - observed_at <= FRESHNESS_WINDOW else "stale"
    return TrendSignal(id=record["_id"], title=record["title"], source_url=record["source_url"], observed_at=observed_at, niche_relevance=record["niche_relevance"], geographic_relevance=record["geographic_relevance"], source_type=record["source_type"], retrieved_at=record["retrieved_at"], freshness=freshness)


@router.get("/trends", response_model=TrendFeedResponse)
def list_signals(user: dict = Depends(current_user), repo: TrendRepository = Depends(repository)) -> TrendFeedResponse:
    signals = [as_signal(record) for record in repo.list_for_owner(user["_id"])]
    if not signals:
        return TrendFeedResponse(status="unavailable", signals=[], fallback="No authorized live trend source is connected. Use creator-history inspiration only; Verdict is not claiming any current trend.", limitations=["Google Trends API access is alpha/application-based and no source credential has been configured.", "Import an attributable, creator-authorized source observation to display it here."])
    return TrendFeedResponse(status="available", signals=signals, fallback=None, limitations=["Signals are source observations, not guarantees of Instagram relevance or performance."])
