from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app
from app.repositories.users import InMemoryUserRepository
from app.services.auth import AuthService


def test_api_sets_security_headers_and_allows_only_configured_origin() -> None:
    settings = Settings(
        mongodb_uri=None,
        session_secret="test-session-secret-that-is-at-least-32-chars",
        web_origins=("https://app.verdict.example",),
    )
    client = TestClient(create_app(AuthService(InMemoryUserRepository(), settings.session_secret), settings=settings))

    response = client.get("/api/v1/health")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert response.headers["cache-control"] == "no-store"

    allowed = client.options(
        "/api/v1/auth/me",
        headers={"Origin": "https://app.verdict.example", "Access-Control-Request-Method": "GET"},
    )
    denied = client.options(
        "/api/v1/auth/me",
        headers={"Origin": "https://untrusted.example", "Access-Control-Request-Method": "GET"},
    )
    assert allowed.headers["access-control-allow-origin"] == "https://app.verdict.example"
    assert denied.status_code == 400


def test_https_deployment_uses_secure_session_cookie() -> None:
    settings = Settings(
        mongodb_uri=None,
        session_secret="test-session-secret-that-is-at-least-32-chars",
        cookie_secure=True,
    )
    client = TestClient(create_app(AuthService(InMemoryUserRepository(), settings.session_secret), settings=settings))

    response = client.post(
        "/api/v1/auth/sign-up",
        json={"email": "creator@example.com", "password": "correct-horse-battery-staple", "display_name": "Creator"},
    )

    assert response.status_code == 201
    assert "Secure" in response.headers["set-cookie"]
    assert "HttpOnly" in response.headers["set-cookie"]
    assert "SameSite=lax" in response.headers["set-cookie"]
