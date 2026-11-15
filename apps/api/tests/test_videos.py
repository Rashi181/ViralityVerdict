import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi.testclient import TestClient

from app.main import create_app
from app.repositories.audience import InMemoryAudienceRepository
from app.repositories.imports import InMemoryImportRepository
from app.repositories.opportunities import InMemoryOpportunityRepository
from app.repositories.trends import InMemoryTrendRepository
from app.repositories.users import InMemoryUserRepository
from app.repositories.videos import InMemoryVideoRepository
from app.services.auth import AuthService
from app.integrations.gemini_reel import GeminiReelAnalysis
from app.schemas.videos import ReelFinding


class FakeReelAnalyzer:
    def __init__(self) -> None:
        self.calls = 0

    def analyze(self, private_video_path: Path, *, content_type: str, duration_seconds: float, frame_paths: list[Path]) -> GeminiReelAnalysis:
        self.calls += 1
        assert private_video_path.is_file()
        assert content_type == "video/mp4"
        assert duration_seconds == 6.0
        assert frame_paths
        return GeminiReelAnalysis(
            findings=[ReelFinding(timestamp_seconds=1.0, focus="hook", severity="medium", observation="A visual opening is present.", recommendation="State the value in the first line.")],
            summary="Test-only structured feedback.",
            limitations=["Test provider result; no external model was called."],
        )


def test_private_video_upload_extracts_real_metadata() -> None:
    app = create_app(AuthService(InMemoryUserRepository(), "test-session-secret-that-is-at-least-32-chars"), InMemoryImportRepository(), InMemoryAudienceRepository(), InMemoryTrendRepository(), InMemoryOpportunityRepository(), InMemoryVideoRepository())
    client = TestClient(app)
    client.post("/api/v1/auth/sign-up", json={"email": "creator@example.com", "password": "correct-horse-battery-staple", "display_name": "Creator"})
    with TemporaryDirectory() as directory:
        path = Path(directory) / "sample.mp4"
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=320x240:d=6", "-pix_fmt", "yuv420p", str(path)], check=True, capture_output=True)
        response = client.post("/api/v1/videos", files={"file": ("sample.mp4", path.read_bytes(), "video/mp4")})
    assert response.status_code == 201
    job = response.json()
    assert job["status"] == "completed"
    assert job["width"] == 320 and job["height"] == 240 and job["duration_seconds"] == 6.0
    analysis = client.get(f"/api/v1/videos/{job['id']}/analysis")
    assert analysis.status_code == 200
    assert analysis.json()["status"] == "awaiting_ai_analysis"
    assert analysis.json()["score"] is None
    assert analysis.json()["attention_risks"] == []
    assert analysis.json()["evidence"][1]["sampled_frame_count"] >= 1


def test_private_video_analysis_is_explicit_owner_scoped_and_persists_structured_result() -> None:
    analyzer = FakeReelAnalyzer()
    app = create_app(AuthService(InMemoryUserRepository(), "test-session-secret-that-is-at-least-32-chars"), InMemoryImportRepository(), InMemoryAudienceRepository(), InMemoryTrendRepository(), InMemoryOpportunityRepository(), InMemoryVideoRepository(), reel_analyzer=analyzer)
    client = TestClient(app)
    client.post("/api/v1/auth/sign-up", json={"email": "creator@example.com", "password": "correct-horse-battery-staple", "display_name": "Creator"})
    with TemporaryDirectory() as directory:
        path = Path(directory) / "sample.mp4"
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=320x240:d=6", "-pix_fmt", "yuv420p", str(path)], check=True, capture_output=True)
        job = client.post("/api/v1/videos", files={"file": ("sample.mp4", path.read_bytes(), "video/mp4")}).json()
    result = client.post(f"/api/v1/videos/{job['id']}/analysis")
    assert result.status_code == 200
    assert result.json()["status"] == "ready"
    assert result.json()["label"] == "Analysis ready"
    assert "provider" not in result.json()["label"].lower()
    assert result.json()["findings"][0]["timestamp_seconds"] == 1.0
    assert result.json()["persona_reactions"] == []
    assert analyzer.calls == 1
    client.post("/api/v1/auth/sign-out")
    client.post("/api/v1/auth/sign-up", json={"email": "other@example.com", "password": "correct-horse-battery-staple", "display_name": "Other"})
    assert client.post(f"/api/v1/videos/{job['id']}/analysis").status_code == 404
