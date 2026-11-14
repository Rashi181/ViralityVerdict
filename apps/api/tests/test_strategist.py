from fastapi.testclient import TestClient
from app.main import create_app
from app.repositories.users import InMemoryUserRepository
from app.services.auth import AuthService
def test_strategist_exposes_scoped_read_tools_without_model_claim() -> None:
 c=TestClient(create_app(AuthService(InMemoryUserRepository(),"test-session-secret-that-is-at-least-32-chars")));c.post("/api/v1/auth/sign-up",json={"email":"a@example.com","password":"correct-horse-battery-staple","display_name":"A"});x=c.get("/api/v1/strategist/tools").json();assert x["status"]=="provider_unavailable" and x["tools"]["plan_count"]==0 and "not generated" in x["limitations"][1]
