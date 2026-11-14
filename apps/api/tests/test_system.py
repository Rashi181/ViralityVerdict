from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_reports_service_identity() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "verdict-api",
        "version": "0.1.0",
    }


def test_ready_is_versioned() -> None:
    response = client.get("/api/v1/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
