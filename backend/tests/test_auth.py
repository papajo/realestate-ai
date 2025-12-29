import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_register(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "Test User"
        }
    )
    assert response.status_code in [201, 400]  # 400 if user exists


@pytest.mark.asyncio
async def test_login(client):
    # First register
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "login_test@example.com",
            "password": "testpassword123",
            "full_name": "Test User"
        }
    )
    
    # Then login
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "login_test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_get_current_user(client):
    # Register and login
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "me_test@example.com",
            "password": "testpassword123",
            "full_name": "Test User"
        }
    )
    
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "me_test@example.com",
            "password": "testpassword123"
        }
    )
    
    token = login_response.json()["access_token"]
    
    # Get current user
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "me_test@example.com"
