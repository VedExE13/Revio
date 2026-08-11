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