from jose import jwt

from app.core.config import settings


def test_register_user_success(client):

    user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    response = client.post(
        "/api/v1/register",
        json=user_data,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    assert "password" not in data
    assert "hashed_password" not in data

def test_register_duplicate_email(client):

    user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    first_response = client.post(
        "/api/v1/register",
        json=user_data,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/v1/register",
        json=user_data,
    )

    assert second_response.status_code == 409

    data = second_response.json()

    assert data["detail"] == "Email already registered"

def test_register_invalid_email(client):

    user_data = {
        "name": "Ved",
        "email": "not-an-email",
        "password": "password123",
    }

    response = client.post(
        "/api/v1/register",
        json=user_data,
    )

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert data["detail"][0]["loc"] == ["body", "email"]
    assert data["detail"][0]["input"] == "not-an-email"

def test_register_short_password(client):

    user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "123",
    }

    response = client.post(
        "/api/v1/register",
        json=user_data,
    )
    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert data["detail"][0]["loc"] == ["body", "password"]
    assert data["detail"][0]["input"] == "123"
    assert data["detail"][0]["type"] == "string_too_short"
    assert data["detail"][0]["ctx"]["min_length"] == 8

def test_login_success(client):
    user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    register_response = client.post(
    "/api/v1/register",
    json=user_data,
    )

    assert register_response.status_code == 201

    login_response = client.post(
    "/api/v1/login",
    data={
        "username": user_data["email"],
        "password": user_data["password"],
        },
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data
    assert data["access_token"]
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):
    user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    register_response = client.post(
        "/api/v1/register",
        json=user_data,
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/login",
        data={
            "username": user_data["email"],
            "password": "wrongpassword",
        },
    )

    assert login_response.status_code == 401

    data = login_response.json()

    assert data["detail"] == "Invalid email or password"

def test_login_nonexistent_user(client):

    login_response = client.post(
        "/api/v1/login",
        data={
            "username": "doesnotexist@example.com",
            "password": "password123",
        },
    )

    assert login_response.status_code == 401

    data = login_response.json()

    assert data["detail"] == "Invalid email or password"

def test_login_returns_valid_jwt(client):
        user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }
        
        register_response = client.post(
            "/api/v1/register",
            json=user_data,
    )   

        assert register_response.status_code == 201

        register_data = register_response.json()

        expected_user_id = register_data["id"]

        login_response = client.post(
        "/api/v1/login",
         data={
            "username": user_data["email"],
            "password": user_data["password"],
    },
)

        assert login_response.status_code == 200

        login_data = login_response.json()

        payload = jwt.decode(
        login_data["access_token"],
        settings.secret_key,
        algorithms=[settings.algorithm],
)
        assert payload["sub"] == str(expected_user_id)
        assert "exp" in payload