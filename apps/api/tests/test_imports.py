from fastapi.testclient import TestClient
from app.main import create_app
from app.repositories.imports import InMemoryImportRepository
from app.repositories.users import InMemoryUserRepository
from app.services.auth import AuthService

def make_client(repo: InMemoryImportRepository) -> TestClient:
    return TestClient(create_app(AuthService(InMemoryUserRepository(), "test-session-secret-that-is-at-least-32-chars"), repo))
def signup(client: TestClient, email: str) -> None:
    assert client.post("/api/v1/auth/sign-up", json={"email": email, "password": "correct-horse-battery-staple", "display_name": email}).status_code == 201
def test_demo_is_labeled_and_private() -> None:
    repo = InMemoryImportRepository(); a, b = make_client(repo), make_client(repo); signup(a, "a@x.com"); signup(b, "b@x.com")
    result = a.post("/api/v1/imports/demo"); assert result.status_code == 201 and result.json()["source"] == "synthetic_demo"
    assert b.get("/api/v1/imports").json() == []

def test_csv_import_validates_and_marks_user_import() -> None:
    client = make_client(InMemoryImportRepository()); signup(client, "csv@x.com")
    content = "media_id,published_at,caption,media_type,views,likes,comments\nrow-1,2026-01-01T00:00:00Z,Hello,reel,10,2,1\n"
    response = client.post("/api/v1/imports/csv", data={"consent_confirmed": "true"}, files={"file": ("media.csv", content, "text/csv")})
    assert response.status_code == 201 and response.json()["source"] == "user_import"
