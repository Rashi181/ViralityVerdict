from fastapi.testclient import TestClient

from app.main import create_app
from app.repositories.users import InMemoryUserRepository
from app.services.auth import AuthService


def client() -> TestClient:
    service = AuthService(InMemoryUserRepository(), "test-session-secret-that-is-at-least-32-chars")
    return TestClient(create_app(service))


def sign_up(client: TestClient, email: str, name: str) -> dict:
    response = client.post("/api/v1/auth/sign-up", json={"email": email, "password": "correct-horse-battery-staple", "display_name": name})
    assert response.status_code == 201
    return response.json()


def test_session_is_required_and_sign_out_revokes_browser_session() -> None:
    browser = client()
    assert browser.get("/api/v1/auth/me").status_code == 401
    user = sign_up(browser, "creator@example.com", "Creator")
    assert browser.get("/api/v1/auth/me").json()["id"] == user["id"]
    assert browser.post("/api/v1/auth/sign-out").status_code == 204
    assert browser.get("/api/v1/auth/me").status_code == 401


def test_user_cannot_read_or_overwrite_another_users_onboarding() -> None:
    creator_a, creator_b = client(), client()
    user_a = sign_up(creator_a, "a@example.com", "A")
    user_b = sign_up(creator_b, "b@example.com", "B")
    payload = {
        "niche": "accessible fitness", "content_goals": ["educate"],
        "posting_constraints": "two hours each week", "preferred_language": "en",
        "preferred_tone": "encouraging", "connection_preference": "manual_import",
    }
    assert creator_a.put("/api/v1/onboarding", json=payload).status_code == 200
    assert creator_b.get(f"/api/v1/users/{user_a['id']}").status_code == 403
    assert creator_b.get("/api/v1/onboarding").status_code == 404
    assert creator_b.get(f"/api/v1/users/{user_b['id']}").status_code == 200
