from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health_returns_200():
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_json():
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_health_post_not_allowed():
    response = client.post("/health")
    assert response.status_code == 405
