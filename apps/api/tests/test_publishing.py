from fastapi.testclient import TestClient
from app.main import create_app
from app.repositories.users import InMemoryUserRepository
from app.services.auth import AuthService
def test_publishing_requires_manual_handoff_without_meta() -> None:
 c=TestClient(create_app(AuthService(InMemoryUserRepository(),"test-session-secret-that-is-at-least-32-chars")));c.post("/api/v1/auth/sign-up",json={"email":"a@example.com","password":"correct-horse-battery-staple","display_name":"A"});x=c.get("/api/v1/publishing/eligibility").json();assert not x["eligible"] and x["status"]=="manual_handoff_required" and "not published" in x["limitations"][1]
