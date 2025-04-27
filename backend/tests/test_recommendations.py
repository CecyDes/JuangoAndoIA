# tests/test_recommendations.py

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_recommendations_existing_user(monkeypatch):
    # Simula un usuario existente con preferencias y un token válido
    user_id = "testuser1"
    token = "testjwttoken"  # Debe ser generado o simulado para pruebas

    # Monkeypatch la autenticación si es necesario
    # monkeypatch.setattr("core.security.get_current_user", lambda: {"sub": user_id})

    response = client.get(
        f"/recommendations/{user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    if response.json():
        assert "game_id" in response.json()[0]

def test_get_recommendations_cold_start(monkeypatch):
    # Simula un usuario sin historial
    user_id = "newuser"
    token = "testjwttoken"

    response = client.get(
        f"/recommendations/{user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
