from typing import Literal
from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter()

class InstagramStatus(BaseModel):
    status: Literal["not_configured", "ready_for_connect"]
    detail: str

@router.get("/instagram/status", response_model=InstagramStatus)
def instagram_status(request: Request) -> InstagramStatus:
    settings = request.app.state.settings
    if not settings.meta_app_id:
        return InstagramStatus(status="not_configured", detail="Meta app credentials have not been configured. Use an authorized import or synthetic demo data.")
    return InstagramStatus(status="ready_for_connect", detail="Meta app configuration exists; OAuth implementation and approval are still required.")
