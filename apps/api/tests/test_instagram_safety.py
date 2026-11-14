from cryptography.fernet import Fernet
from fastapi.testclient import TestClient
import pytest

from app.core.config import Settings
from app.integrations.instagram_policy import validate_api_method, validate_scope_request
from app.main import create_app
from app.repositories.connections import InMemoryConnectionRepository
from app.repositories.users import InMemoryUserRepository
from app.services.auth import AuthService
from app.services.token_vault import TokenVault


def test_instagram_policy_vault_disconnect_and_audit_are_safe_and_owner_scoped() -> None:
    key = Fernet.generate_key().decode()
    vault = TokenVault(key)
    repository = InMemoryConnectionRepository()
    app = create_app(
        AuthService(InMemoryUserRepository(), "test-session-secret-that-is-at-least-32-chars"),
        settings=Settings(None, "test-session-secret-that-is-at-least-32-chars", meta_token_encryption_key=key),
        connection_repository=repository,
    )
    owner, other = TestClient(app), TestClient(app)
    for client, email in ((owner, "owner@example.com"), (other, "other@example.com")):
        assert client.post("/api/v1/auth/sign-up", json={"email": email, "password": "correct-horse-battery-staple", "display_name": "Creator"}).status_code == 201

    raw_token = "never-return-this-raw-token"
    encrypted = vault.encrypt(raw_token)
    assert encrypted != raw_token
    assert vault.decrypt(encrypted) == raw_token
    owner_id = owner.get("/api/v1/auth/me").json()["id"]
    repository.save_connection(owner_id, encrypted, ["instagram_business_basic"])

    safety = owner.get("/api/v1/instagram/safety").json()
    assert safety["requested_scopes"] == ["instagram_business_basic"]
    assert safety["allowed_http_methods"] == ["GET"]
    assert "instagram_business_content_publishing" in safety["denied_scopes"]
    with pytest.raises(ValueError):
        validate_scope_request({"instagram_business_content_publishing"})
    with pytest.raises(ValueError):
        validate_api_method("POST")

    assert owner.post("/api/v1/instagram/disconnect").status_code == 204
    assert repository.connection_for_owner(owner_id) is None
    owner_audit = owner.get("/api/v1/instagram/audit").json()
    assert owner_audit[0]["action"] == "instagram_disconnect"
    assert raw_token not in str(owner_audit)
    assert other.get("/api/v1/instagram/audit").json() == []
