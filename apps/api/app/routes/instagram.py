from typing import Literal
from fastapi import APIRouter, Depends, Request, status
from pydantic import BaseModel

from app.integrations.instagram_policy import ALLOWED_HTTP_METHODS, DENIED_SCOPES, READ_ONLY_SCOPES
from app.repositories.connections import ConnectionRepository
from app.routes.auth import current_user

router = APIRouter()

class InstagramStatus(BaseModel):
    status: Literal["not_configured", "ready_for_connect"]
    detail: str


class InstagramSafety(BaseModel):
    requested_scopes: list[str]
    denied_scopes: list[str]
    allowed_http_methods: list[str]
    publishing: Literal["permanently_manual_only"]


class AuditEntry(BaseModel):
    action: str
    details: dict


def connections(request: Request) -> ConnectionRepository:
    return request.app.state.connection_repository

@router.get("/instagram/status", response_model=InstagramStatus)
def instagram_status(request: Request) -> InstagramStatus:
    settings = request.app.state.settings
    configured = all([settings.meta_app_id, settings.meta_app_secret, settings.meta_instagram_login_config_id, settings.meta_redirect_uri, settings.meta_token_encryption_key])
    if not configured:
        return InstagramStatus(status="not_configured", detail="Instagram Login configuration is incomplete. CSV remains an authorized fallback; Verdict will not claim a live connection.")
    return InstagramStatus(status="ready_for_connect", detail="Instagram Login configuration and encrypted-token storage are ready. OAuth is not enabled until its state/redirect flow is reviewed; publishing remains permanently manual-only.")


@router.get("/instagram/safety", response_model=InstagramSafety)
def instagram_safety() -> InstagramSafety:
    return InstagramSafety(requested_scopes=sorted(READ_ONLY_SCOPES), denied_scopes=sorted(DENIED_SCOPES), allowed_http_methods=sorted(ALLOWED_HTTP_METHODS), publishing="permanently_manual_only")


@router.post("/instagram/disconnect", status_code=status.HTTP_204_NO_CONTENT)
def disconnect_instagram(user: dict = Depends(current_user), repo: ConnectionRepository = Depends(connections)) -> None:
    removed = repo.disconnect(user["_id"])
    repo.add_audit(user["_id"], "instagram_disconnect", {"stored_connection_removed": removed, "remote_revocation": "not_attempted_without_live_oauth"})


@router.get("/instagram/audit", response_model=list[AuditEntry])
def instagram_audit(user: dict = Depends(current_user), repo: ConnectionRepository = Depends(connections)) -> list[AuditEntry]:
    return [AuditEntry(action=entry["action"], details=entry["details"]) for entry in repo.audit_for_owner(user["_id"])]
