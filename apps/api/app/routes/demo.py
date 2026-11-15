from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from app.repositories.audience import AudienceRepository
from app.repositories.imports import ImportRepository
from app.routes.auth import current_user
from app.services.demo_fixture import DemoFixtureError, load_demo_fixture

router = APIRouter()


class DemoStatus(BaseModel):
    available: bool
    detail: str


class DemoLoadResponse(BaseModel):
    status: str
    media_count: int
    aggregate_count: int
    limitations: list[str]


def _enabled(request: Request) -> bool:
    settings = request.app.state.settings
    return bool(settings.demo_mode and settings.demo_fixture_path)


@router.get("/demo/status", response_model=DemoStatus)
def status(request: Request, user: dict = Depends(current_user)) -> DemoStatus:
    del user
    if not _enabled(request):
        return DemoStatus(available=False, detail="Synthetic demonstration mode is disabled.")
    return DemoStatus(available=True, detail="Synthetic demonstration data is available for this local workspace only.")


@router.post("/demo/load-fixture", response_model=DemoLoadResponse)
def load_fixture(request: Request, user: dict = Depends(current_user)) -> DemoLoadResponse:
    if not _enabled(request):
        raise HTTPException(status_code=404, detail="Synthetic demonstration mode is disabled.")
    imports: ImportRepository = request.app.state.import_repository
    audience: AudienceRepository = request.app.state.audience_repository
    existing = [record for record in imports.list_for_owner(user["_id"]) if record["source"] == "synthetic_demo"]
    if existing:
        existing_audience = audience.latest_for_owner(user["_id"])
        aggregate_count = len(existing_audience["aggregates"]) if existing_audience and all(item["source"] == "synthetic_demo" for item in existing_audience["aggregates"]) else 0
        return DemoLoadResponse(status="already_loaded", media_count=len(existing[0]["media"]), aggregate_count=aggregate_count, limitations=existing[0]["limitations"])
    try:
        media, aggregates, limitations = load_demo_fixture(request.app.state.settings.demo_fixture_path)
    except DemoFixtureError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    imports.create(user["_id"], "synthetic_demo", media, limitations)
    audience.create(user["_id"], aggregates, limitations)
    return DemoLoadResponse(status="loaded", media_count=len(media), aggregate_count=len(aggregates), limitations=limitations)
