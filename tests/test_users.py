import pytest
from fastapi.testclient import TestClient


def test_get_user(client: TestClient, test_user):
    """Test de récupération des informations d'un utilisateur."""
    response = client.get(f"/api/v1/users/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_get_nonexistent_user(client: TestClient):
    """Test de récupération d'un utilisateur inexistant."""
    fake_uuid = "12345678-1234-5678-1234-567812345678"
    response = client.get(f"/api/v1/users/{fake_uuid}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"