from fastapi.testclient import TestClient
from app.main import create_app
from app.repositories.users import InMemoryUserRepository
from app.services.auth import AuthService

def test_caption_studio_returns_general_captions_and_honest_hashtags() -> None:
    client=TestClient(create_app(AuthService(InMemoryUserRepository(),"test-session-secret-that-is-at-least-32-chars")))
    client.post("/api/v1/auth/sign-up",json={"email":"creator@example.com","password":"correct-horse-battery-staple","display_name":"Creator"})
    response=client.post("/api/v1/optimize",json={"draft_text":"Three editing shortcuts for creators","call_to_action":"Save this for later.","refinement_prompt":"Make it friendly."})
    assert response.status_code==200
    result=response.json()
    assert [caption["id"] for caption in result["captions"]]==["concise","context_first","question_led"]
    assert result["hashtags"] and result["hashtags"][0]["source"]=="creator_provided_keyword"
    assert "not a claim that this hashtag is trending" in result["hashtags"][0]["explanation"]
    assert "cannot" in result["limitations"][0]
    assert result["persona_reactions"]==[]
