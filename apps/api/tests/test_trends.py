from fastapi.testclient import TestClient

from app.main import create_app
from app.repositories.audience import InMemoryAudienceRepository
from app.repositories.imports import InMemoryImportRepository
from app.repositories.trends import InMemoryTrendRepository
from app.repositories.users import InMemoryUserRepository
from app.services.auth import AuthService


def client_for(repository: InMemoryTrendRepository) -> TestClient:
    return TestClient(create_app(AuthService(InMemoryUserRepository(), "test-session-secret-that-is-at-least-32-chars"), InMemoryImportRepository(), InMemoryAudienceRepository(), repository))


def sign_up(client: TestClient, email: str) -> None:
    assert client.post("/api/v1/auth/sign-up", json={"email": email, "password": "correct-horse-battery-staple", "display_name": "Creator"}).status_code == 201


def test_trends_are_unavailable_without_a_source() -> None:
    client = client_for(InMemoryTrendRepository())
    sign_up(client, "creator@example.com")
    feed = client.get("/api/v1/trends").json()
    assert feed["status"] == "unavailable"
    assert feed["signals"] == []
    assert "not claiming any current trend" in feed["fallback"]


def test_imported_trends_have_provenance_freshness_and_owner_scope() -> None:
    repository = InMemoryTrendRepository()
    creator = client_for(repository)
    other = client_for(repository)
    sign_up(creator, "creator@example.com")
    sign_up(other, "other@example.com")
    response = creator.post("/api/v1/trends/import", json={"consent_confirmed": True, "signals": [{"title": "Search interest observation", "source_url": "https://trends.google.com/trends/", "observed_at": "2026-11-13T12:00:00Z", "niche_relevance": "Creator supplied a relevant search observation.", "geographic_relevance": "US", "source_type": "google_trends"}]})
    assert response.status_code == 201
    signal = creator.get("/api/v1/trends").json()["signals"][0]
    assert signal["freshness"] == "current"
    assert signal["source_url"] == "https://trends.google.com/trends/"
    assert other.get("/api/v1/trends").json()["status"] == "unavailable"
