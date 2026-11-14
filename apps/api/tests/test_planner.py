from fastapi.testclient import TestClient
from app.main import create_app
from app.repositories.users import InMemoryUserRepository
from app.services.auth import AuthService

def test_plans_are_owner_scoped() -> None:
 app=create_app(AuthService(InMemoryUserRepository(),"test-session-secret-that-is-at-least-32-chars")); a,b=TestClient(app),TestClient(app)
 for client,email in ((a,"a@example.com"),(b,"b@example.com")):client.post("/api/v1/auth/sign-up",json={"email":email,"password":"correct-horse-battery-staple","display_name":"Creator"})
 created=a.post("/api/v1/plans",json={"title":"Test draft","status":"scheduled","planned_at":"2026-11-15T12:00:00Z"})
 assert created.status_code==201 and created.json()["status"]=="scheduled"
 assert len(a.get("/api/v1/plans").json())==1 and b.get("/api/v1/plans").json()==[]
