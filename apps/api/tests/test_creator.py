from fastapi.testclient import TestClient

from app.main import create_app
from app.repositories.imports import InMemoryImportRepository
from app.repositories.users import InMemoryUserRepository
from app.services.auth import AuthService


def test_creator_summary_deduplicates_owner_media() -> None:
    repository = InMemoryImportRepository()
    client = TestClient(create_app(
        AuthService(InMemoryUserRepository(), "test-session-secret-that-is-at-least-32-chars"),
        repository,
    ))
    client.post("/api/v1/auth/sign-up", json={
        "email": "a@x.com", "password": "correct-horse-battery-staple", "display_name": "A",
    })
    client.post("/api/v1/imports/demo")
    client.post("/api/v1/imports/demo")

    summary = client.get("/api/v1/creator/profile").json()

    assert summary["sample_size"] == 1
    assert summary["top_media_ids"] == ["demo-reel-001"]
    assert summary["recurring_formats"] == {"reel": 1}
    assert summary["hook_samples"] == ["Synthetic demo: three quick editing tips."]
    assert "Sparse history" in summary["limitations"][1]
