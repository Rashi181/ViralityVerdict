from datetime import UTC, datetime
import secrets
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from app.integrations.instagram_policy import ALLOWED_HTTP_METHODS, DENIED_SCOPES, READ_ONLY_SCOPES
from app.integrations.meta_oauth import FacebookLoginMetaClient, MetaClient
from app.repositories.connections import ConnectionRepository
from app.routes.auth import current_user
from app.services.token_vault import TokenVault

router = APIRouter()

class InstagramStatus(BaseModel):
    status: Literal["not_configured", "ready_for_connect", "connected"]
    detail: str
    last_synced_at: datetime | None = None
class InstagramSafety(BaseModel):
    requested_scopes: list[str]; denied_scopes: list[str]; allowed_http_methods: list[str]; publishing: Literal["permanently_manual_only"]
class SyncResponse(BaseModel):
    status: Literal["completed"]; media_count: int; account_id: str; username: str | None; limitations: list[str]
class AuditEntry(BaseModel): action: str; details: dict

def connections(request: Request) -> ConnectionRepository: return request.app.state.connection_repository
def configured(request: Request) -> bool:
    s = request.app.state.settings
    return all([s.meta_app_id, s.meta_app_secret, s.meta_redirect_uri, s.meta_token_encryption_key])
def client(request: Request) -> MetaClient:
    if not configured(request): raise HTTPException(503, "Instagram connection is not configured. Add the approved local Meta credentials first.")
    if hasattr(request.app.state, "meta_client"): return request.app.state.meta_client
    s = request.app.state.settings
    return FacebookLoginMetaClient(s.meta_app_id, s.meta_app_secret, s.meta_redirect_uri, s.meta_api_version)  # type: ignore[arg-type]
def vault(request: Request) -> TokenVault:
    key = request.app.state.settings.meta_token_encryption_key
    if not key: raise HTTPException(503, "Token encryption is not configured")
    return TokenVault(key)

@router.get("/instagram/status", response_model=InstagramStatus)
def instagram_status(request: Request, user: dict = Depends(current_user), repo: ConnectionRepository = Depends(connections)) -> InstagramStatus:
    record = repo.connection_for_owner(user["_id"])
    if record: return InstagramStatus(status="connected", detail="Instagram is connected with read-only access. Sync only imports eligible observed data.", last_synced_at=record.get("last_synced_at"))
    if not configured(request): return InstagramStatus(status="not_configured", detail="Official Meta OAuth is not configured locally. Verdict has no Instagram access.")
    return InstagramStatus(status="ready_for_connect", detail="Ready to open Meta's read-only consent screen. Verdict never requests publishing, messages, comments, or account-edit access.")

@router.get("/instagram/connect")
def connect_instagram(request: Request, user: dict = Depends(current_user), repo: ConnectionRepository = Depends(connections)) -> RedirectResponse:
    state = secrets.token_urlsafe(32); repo.save_oauth_state(user["_id"], state)
    return RedirectResponse(client(request).authorization_url(state), status_code=302)

@router.get("/instagram/callback")
def instagram_callback(request: Request, code: str | None = None, state: str | None = None, error: str | None = None, repo: ConnectionRepository = Depends(connections)) -> RedirectResponse:
    owner_id = repo.consume_oauth_state(state or "")
    target = request.app.state.settings.web_origins[0].rstrip("/") + "/connect"
    if not owner_id or error or not code: return RedirectResponse(target + "?instagram=cancelled", status_code=302)
    try:
        token = client(request).exchange_code(code)
        repo.save_connection(owner_id, vault(request).encrypt(token), sorted(READ_ONLY_SCOPES))
        repo.add_audit(owner_id, "instagram_connected", {"scopes": sorted(READ_ONLY_SCOPES), "token": "redacted"})
        return RedirectResponse(target + "?instagram=connected", status_code=302)
    except ValueError:
        return RedirectResponse(target + "?instagram=failed", status_code=302)

@router.post("/instagram/sync", response_model=SyncResponse)
def sync_instagram(request: Request, user: dict = Depends(current_user), repo: ConnectionRepository = Depends(connections)) -> SyncResponse:
    record = repo.connection_for_owner(user["_id"])
    if not record: raise HTTPException(409, "Connect Instagram before syncing")
    try:
        snapshot = client(request).read_snapshot(vault(request).decrypt(record["encrypted_token"]))
    except ValueError as exc:
        # A missing Page/Professional-Instagram link is recoverable setup
        # state, not an internal error. Provider tokens are never exposed.
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    media = []
    for item in snapshot.media:
        if not item.get("id") or not item.get("timestamp"): continue
        media.append({"media_id": str(item["id"]), "published_at": item["timestamp"], "caption": item.get("caption") or "", "media_type": "reel" if str(item.get("media_product_type")).upper() == "REELS" else "post", "views": int(item.get("views") or 0), "likes": int(item.get("like_count") or 0), "comments": int(item.get("comments_count") or 0)})
    if media: request.app.state.import_repository.create(user["_id"], "instagram_api", media, ["Observed through the creator-authorized Meta API. A zero metric means Meta did not return that field; it is not inferred."])
    repo.add_audit(user["_id"], "instagram_sync", {"account_id": snapshot.account_id, "media_count": len(media), "token": "redacted"})
    return SyncResponse(status="completed", media_count=len(media), account_id=snapshot.account_id, username=snapshot.username, limitations=["Only fields returned by Meta were imported. Audience demographics are not claimed unless Meta returns eligible aggregate insight fields."])

@router.get("/instagram/safety", response_model=InstagramSafety)
def instagram_safety() -> InstagramSafety: return InstagramSafety(requested_scopes=sorted(READ_ONLY_SCOPES), denied_scopes=sorted(DENIED_SCOPES), allowed_http_methods=sorted(ALLOWED_HTTP_METHODS), publishing="permanently_manual_only")
@router.post("/instagram/disconnect", status_code=status.HTTP_204_NO_CONTENT)
def disconnect_instagram(user: dict = Depends(current_user), repo: ConnectionRepository = Depends(connections)) -> None:
    removed = repo.disconnect(user["_id"]); repo.add_audit(user["_id"], "instagram_disconnect", {"stored_connection_removed": removed, "remote_revocation": "pending_documented_provider_revoke"})
@router.get("/instagram/audit", response_model=list[AuditEntry])
def instagram_audit(user: dict = Depends(current_user), repo: ConnectionRepository = Depends(connections)) -> list[AuditEntry]: return [AuditEntry(action=e["action"], details=e["details"]) for e in repo.audit_for_owner(user["_id"])]
