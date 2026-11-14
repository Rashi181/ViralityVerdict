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
    configured = all([settings.meta_app_id, settings.meta_app_secret, settings.meta_instagram_login_config_id, settings.meta_redirect_uri])
    if not configured:
        return InstagramStatus(status="not_configured", detail="Instagram Login configuration is incomplete. CSV remains an authorized fallback; Verdict will not claim a live connection.")
    return InstagramStatus(status="ready_for_connect", detail="Instagram Login configuration exists. The app will request read/sync access only; publishing remains permanently manual-only.")
