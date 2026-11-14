from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    service: Literal["verdict-api"] = "verdict-api"
    version: str = "0.1.0"


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse()


@router.get("/ready", response_model=HealthResponse)
async def ready() -> HealthResponse:
    """M0 readiness: external dependencies are intentionally not initialized yet."""
    return HealthResponse()
