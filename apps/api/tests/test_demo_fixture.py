import json

from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app
from app.repositories.audience import InMemoryAudienceRepository
from app.repositories.imports import InMemoryImportRepository
from app.repositories.users import InMemoryUserRepository
from app.services.auth import AuthService


def _fixture(path) -> None:
    path.write_text(json.dumps({
        "source": {"type": "synthetic_demo_fixture", "as_of": "2026-11-15T00:00:00Z"},
        "posts": [{
            "id": "demo-1", "published_at": "2026-10-01T00:00:00Z", "format": "reel",
            "caption": "Build a clearer data workflow #creator #datatips", "hashtags": ["creator", "datatips"],
            "keywords": ["workflow", "data"],
            "metrics": {"views": 120, "likes": 12, "comments": 3, "saves": 4, "shares": 2},
        }],
        "audience": {
            "total_followers": 100, "age_distribution_pct": {"25-34": 60},
            "top_countries_pct": {"US": 65}, "interest_affinities_demo_estimates": {"Forbidden": 100},
        },
        "synthetic_audience_personas": [{"name": "Forbidden Persona"}],
        "content_taxonomy": {"niche": "Forbidden niche"},
        "recommendation_test_cases": [{"recommendation": "Forbidden recommendation"}],
    }), encoding="utf-8")


def _sign_up(client: TestClient, email: str) -> None:
    response = client.post("/api/v1/auth/sign-up", json={
        "email": email, "password": "correct-horse-battery-staple", "display_name": "Creator",
    })
    assert response.status_code == 201


def test_demo_fixture_uses_raw_facts_only_and_is_owner_scoped(tmp_path) -> None:
    fixture_path = tmp_path / "fixture.json"
    _fixture(fixture_path)
    settings = Settings(
        mongodb_uri=None, session_secret="test-session-secret-that-is-at-least-32-chars",
        demo_mode=True, demo_fixture_path=str(fixture_path),
    )
    app = create_app(
        AuthService(InMemoryUserRepository(), settings.session_secret),
        InMemoryImportRepository(), InMemoryAudienceRepository(), settings=settings,
    )
    owner, other = TestClient(app), TestClient(app)
    _sign_up(owner, "owner@example.com")
    _sign_up(other, "other@example.com")

    assert owner.get("/api/v1/demo/status").json()["available"] is True
    loaded = owner.post("/api/v1/demo/load-fixture")
    assert loaded.status_code == 200
    assert loaded.json()["media_count"] == 1
    assert loaded.json()["aggregate_count"] == 3
    assert owner.post("/api/v1/demo/load-fixture").json()["status"] == "already_loaded"

    creator = owner.get("/api/v1/creator/profile").json()
    persona = owner.get("/api/v1/audience/personas/current").json()
    serialized = json.dumps({"creator": creator, "persona": persona})
    assert creator["data_source"] == "synthetic_demo"
    assert persona["status"] == "synthetic_demo"
    assert len(persona["personas"]) == 1
    assert persona["personas"][0]["label"] == "Workflow + Data learner · 25-34"
    assert "Aggregate age band 25-34: 60%" in persona["personas"][0]["observed_evidence"][0]
    assert "datatips" in serialized.lower()
    assert "Forbidden Persona" not in serialized
    assert "Forbidden niche" not in serialized
    assert "Forbidden recommendation" not in serialized
    assert other.get("/api/v1/creator/profile").json()["sample_size"] == 0
    assert other.get("/api/v1/audience/personas/current").json()["status"] == "provisional"


def test_demo_fixture_route_is_hidden_when_disabled(tmp_path) -> None:
    fixture_path = tmp_path / "fixture.json"
    _fixture(fixture_path)
    settings = Settings(
        mongodb_uri=None, session_secret="test-session-secret-that-is-at-least-32-chars",
        demo_mode=False, demo_fixture_path=str(fixture_path),
    )
    client = TestClient(create_app(AuthService(InMemoryUserRepository(), settings.session_secret), settings=settings))
    _sign_up(client, "owner@example.com")
    assert client.get("/api/v1/demo/status").json()["available"] is False
    assert client.post("/api/v1/demo/load-fixture").status_code == 404
