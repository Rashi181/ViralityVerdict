from fastapi.testclient import TestClient

from app.main import create_app
from app.repositories.audience import InMemoryAudienceRepository
from app.repositories.imports import InMemoryImportRepository
from app.repositories.users import InMemoryUserRepository
from app.services.auth import AuthService


def build_client() -> TestClient:
    return TestClient(create_app(
        AuthService(InMemoryUserRepository(), "test-session-secret-that-is-at-least-32-chars"),
        InMemoryImportRepository(), InMemoryAudienceRepository(),
    ))


def sign_up(client: TestClient, email: str) -> None:
    response = client.post("/api/v1/auth/sign-up", json={
        "email": email, "password": "correct-horse-battery-staple", "display_name": "Creator",
    })
    assert response.status_code == 201


def test_persona_is_provisional_without_aggregate_audience_data() -> None:
    client = build_client()
    sign_up(client, "creator@example.com")

    persona = client.get("/api/v1/audience/personas/current")

    assert persona.status_code == 200
    assert persona.json()["status"] == "provisional"
    assert persona.json()["observed_evidence"] == []
    assert "demographics" in persona.json()["unknowns"][0]


def test_audience_evidence_is_owner_scoped_and_feedback_persists() -> None:
    audience_repository = InMemoryAudienceRepository()
    app = create_app(
        AuthService(InMemoryUserRepository(), "test-session-secret-that-is-at-least-32-chars"),
        InMemoryImportRepository(), audience_repository,
    )
    creator = TestClient(app)
    other_creator = TestClient(app)
    sign_up(creator, "creator@example.com")
    sign_up(other_creator, "other@example.com")
    imported = creator.post("/api/v1/audience/import", json={
        "consent_confirmed": True,
        "aggregates": [{
            "field": "top_locations", "values": {"Boston": 64}, "source": "user_import",
            "source_label": "Authorized Instagram audience export", "as_of": "2026-11-13T12:00:00Z",
        }],
    })

    assert imported.status_code == 201
    assert creator.post("/api/v1/audience/personas/feedback", json={"note": "Prioritize short tutorials."}).status_code == 204
    persona = creator.get("/api/v1/audience/personas/current").json()
    other_persona = other_creator.get("/api/v1/audience/personas/current").json()

    assert persona["status"] == "observed"
    assert persona["observed_evidence"][0]["values"] == {"Boston": 64}
    assert persona["feedback_note"] == "Prioritize short tutorials."
    assert other_persona["status"] == "provisional"
    assert other_persona["observed_evidence"] == []
