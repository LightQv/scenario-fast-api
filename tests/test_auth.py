import pytest
from fastapi.testclient import TestClient


def test_register_user(client: TestClient):
    """Test d'inscription d'un nouvel utilisateur."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "confirm_password": "password123"
        }
    )
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"


def test_register_user_duplicate_email(client: TestClient, test_user):
    """Test d'inscription avec un email déjà existant."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "anothuser",
            "email": "test@example.com",  # Email déjà utilisé
            "password": "password123",
            "confirm_password": "password123"
        }
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_login_user(client: TestClient, test_user):
    """Test de connexion d'un utilisateur."""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "access_token" in response.cookies


def test_login_invalid_credentials(client: TestClient, test_user):
    """Test de connexion avec des identifiants invalides."""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_logout_user(client: TestClient):
    """Test de déconnexion."""
    response = client.get("/api/v1/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully"