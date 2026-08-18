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
    print(data)