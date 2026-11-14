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


def test_private_video_upload_extracts_real_metadata() -> None:
    app = create_app(AuthService(InMemoryUserRepository(), "test-session-secret-that-is-at-least-32-chars"), InMemoryImportRepository(), InMemoryAudienceRepository(), InMemoryTrendRepository(), InMemoryOpportunityRepository(), InMemoryVideoRepository())
    client = TestClient(app)
    client.post("/api/v1/auth/sign-up", json={"email": "creator@example.com", "password": "correct-horse-battery-staple", "display_name": "Creator"})
    with TemporaryDirectory() as directory:
        path = Path(directory) / "sample.mp4"
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=320x240:d=1", "-pix_fmt", "yuv420p", str(path)], check=True, capture_output=True)
        response = client.post("/api/v1/videos", files={"file": ("sample.mp4", path.read_bytes(), "video/mp4")})
    assert response.status_code == 201
    job = response.json()
    assert job["status"] == "completed"
    assert job["width"] == 320 and job["height"] == 240 and job["duration_seconds"] == 1.0
