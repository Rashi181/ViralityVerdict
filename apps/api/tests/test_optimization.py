from fastapi.testclient import TestClient
from app.main import create_app
from app.repositories.users import InMemoryUserRepository
from app.services.auth import AuthService

def test_optimizer_has_exactly_four_labeled_caption_styles() -> None:
    client=TestClient(create_app(AuthService(InMemoryUserRepository(),"test-session-secret-that-is-at-least-32-chars")))
    client.post("/api/v1/auth/sign-up",json={"email":"creator@example.com","password":"correct-horse-battery-staple","display_name":"Creator"})
    response=client.post("/api/v1/optimize",json={"draft_text":"Three editing shortcuts","call_to_action":"Save this for later."})
    assert response.status_code==200
    result=response.json()
    assert [caption["style"] for caption in result["captions"]]==["formal","sarcastic","humorous-tech","humorous-non-tech"]
    assert result["persona_reactions"]==[]
