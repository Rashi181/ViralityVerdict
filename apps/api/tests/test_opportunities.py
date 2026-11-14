from fastapi.testclient import TestClient

from app.main import create_app
from app.repositories.audience import InMemoryAudienceRepository
from app.repositories.imports import InMemoryImportRepository
from app.repositories.opportunities import InMemoryOpportunityRepository
from app.repositories.trends import InMemoryTrendRepository
from app.repositories.users import InMemoryUserRepository
from app.services.auth import AuthService


def test_opportunity_score_is_reproducible_and_owner_scoped() -> None:
    repository = InMemoryOpportunityRepository()
    app = create_app(AuthService(InMemoryUserRepository(), "test-session-secret-that-is-at-least-32-chars"), InMemoryImportRepository(), InMemoryAudienceRepository(), InMemoryTrendRepository(), repository)
    first, second = TestClient(app), TestClient(app)
    for client, email in ((first, "first@example.com"), (second, "second@example.com")):
        assert client.post("/api/v1/auth/sign-up", json={"email": email, "password": "correct-horse-battery-staple", "display_name": "Creator"}).status_code == 201
    payload = {"title": "Tutorial follow-up", "angle": "Build on an observed creator format.", "hook": "Try this next.", "format": "reel", "effort": "low", "evidence": ["creator media ID demo-reel-001"], "score_inputs": {"audience_fit": 80, "trend_relevance": 60, "novelty": 50, "feasibility": 90, "missing_components": ["live trend source"]}}
    created = first.post("/api/v1/opportunities", json=payload).json()
    assert created["score"] == 69.5
    assert created["confidence"] == "reduced"
    assert len(first.get("/api/v1/opportunities").json()) == 1
    assert second.get("/api/v1/opportunities").json() == []
