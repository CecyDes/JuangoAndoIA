# tests/test_feedback.py

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_submit_feedback_success(monkeypatch):
    # Simula autenticación
    user_id = "testuser1"
    token = "testjwttoken"

    feedback_payload = {
        "game_id": "game123",
        "rating": 5,
        "interaction_type": "click"
    }

    response = client.post(
        "/feedback/",
        json=feedback_payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "feedback_id" in response.json()

def test_submit_feedback_invalid_rating(monkeypatch):
    user_id = "testuser1"
    token = "testjwttoken"

    feedback_payload = {
        "game_id": "game123",
        "rating": 10,  # Rating fuera de rango
        "interaction_type": "click"
    }

    response = client.post(
        "/feedback/",
        json=feedback_payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422  # Unprocessable Entity
