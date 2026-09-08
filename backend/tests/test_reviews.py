from tests.conftest import TestSessionLocal
from app.models.review import Review
from app.models.user import User

def test_create_review_success(client): 
    user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    # Register
    register_response = client.post(
        "/api/v1/register",
        json=user_data,
    )
    assert register_response.status_code == 201

    # Login
    login_response = client.post(
        "/api/v1/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    review_data = {
        "title": "Great product",
        "rating": 5,
        "feedback": "Really liked this product.",
    }

    response = client.post(
        "/api/v1/review",
        json=review_data,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == review_data["title"]
    assert data["rating"] == review_data["rating"]
    assert data["feedback"] == review_data["feedback"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    assert "user" in data

def test_create_review_saved_to_database(client):
    user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    client.post(
        "/api/v1/register",
        json=user_data,
    )

    login_response = client.post(
        "/api/v1/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    token = login_response.json()["access_token"]

    review_data = {
        "title": "Amazing product",
        "rating": 4,
        "feedback": "Works really well.",
    }

    response = client.post(
        "/api/v1/review",
        json=review_data,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

    response_data = response.json()

    db = TestSessionLocal()

    try:
        review = (
            db.query(Review)
            .filter(Review.id == response_data["id"])
            .first()
        )

        user = (
            db.query(User)
            .filter(User.email == user_data["email"])
            .first()
        )

        assert review is not None
        assert review.title == review_data["title"]
        assert review.rating == review_data["rating"]
        assert review.feedback == review_data["feedback"]
        assert review.user_id == user.id

    finally:
        db.close()

def test_create_review_requires_auth(client):
    review_data = {
        "title": "Great product",
        "rating": 5,
        "feedback": "Really liked this product.",
    }

    response = client.post(
        "/api/v1/review",
        json=review_data,
    )

    assert response.status_code == 401

def test_create_review_invalid_low_rating(client):
    user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    client.post("/api/v1/register", json=user_data)

    login_response = client.post(
        "/api/v1/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/api/v1/review",
        json={
            "title": "Bad rating",
            "rating": 0,
            "feedback": "Invalid rating.",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422

def test_create_review_invalid_high_rating(client):
    user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    client.post("/api/v1/register", json=user_data)

    login_response = client.post(
        "/api/v1/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/api/v1/review",
        json={
            "title": "Bad rating",
            "rating": 6,
            "feedback": "Invalid rating.",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422

def test_get_reviews(client):
    user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    client.post("/api/v1/register", json=user_data)

    login_response = client.post(
        "/api/v1/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
    }

    client.post(
        "/api/v1/review",
        json={
            "title": "Great product",
            "rating": 5,
            "feedback": "Really enjoyed it.",
        },
        headers=headers,
    )

    client.post(
        "/api/v1/review",
        json={
            "title": "Average product",
            "rating": 3,
            "feedback": "It was okay.",
        },
        headers=headers,
    )

    response = client.get("/api/v1/reviews")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "Great product"
    assert data[1]["title"] == "Average product"

def test_get_reviews_search(client):
    user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    client.post("/api/v1/register", json=user_data)

    login_response = client.post(
        "/api/v1/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
    }

    client.post(
        "/api/v1/review",
        json={
            "title": "Amazing headphones",
            "rating": 5,
            "feedback": "Excellent sound quality.",
        },
        headers=headers,
    )

    client.post(
        "/api/v1/review",
        json={
            "title": "Bad keyboard",
            "rating": 2,
            "feedback": "Keys feel cheap.",
        },
        headers=headers,
    )

    response = client.get(
        "/api/v1/reviews",
        params={"search": "headphones"},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Amazing headphones"

def test_get_reviews_sort_newest(client):
    user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    client.post("/api/v1/register", json=user_data)

    login_response = client.post(
        "/api/v1/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/api/v1/review",
        json={
            "title": "First review",
            "rating": 3,
            "feedback": "First.",
        },
        headers=headers,
    )

    client.post(
        "/api/v1/review",
        json={
            "title": "Second review",
            "rating": 5,
            "feedback": "Second.",
        },
        headers=headers,
    )

    response = client.get(
        "/api/v1/reviews",
        params={"sort": "newest"},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "Second review"
    assert data[1]["title"] == "First review"

def test_get_reviews_sort_oldest(client):
    user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    client.post("/api/v1/register", json=user_data)

    login_response = client.post(
        "/api/v1/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/api/v1/review",
        json={
            "title": "First review",
            "rating": 3,
            "feedback": "First.",
        },
        headers=headers,
    )

    client.post(
        "/api/v1/review",
        json={
            "title": "Second review",
            "rating": 5,
            "feedback": "Second.",
        },
        headers=headers,
    )

    response = client.get(
        "/api/v1/reviews",
        params={"sort": "oldest"},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "First review"
    assert data[1]["title"] == "Second review"

def test_get_reviews_pagination(client):
    user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    client.post("/api/v1/register", json=user_data)

    login_response = client.post(
        "/api/v1/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    for i in range(4):
        client.post(
            "/api/v1/review",
            json={
                "title": f"Review {i}",
                "rating": 5,
                "feedback": f"Feedback {i}",
            },
            headers=headers,
        )

    response = client.get(
        "/api/v1/reviews",
        params={
            "skip": 1,
            "limit": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "Review 1"
    assert data[1]["title"] == "Review 2"

def test_get_my_reviews(client):
    # User 1
    user1 = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    client.post("/api/v1/register", json=user1)

    login1 = client.post(
        "/api/v1/login",
        data={
            "username": user1["email"],
            "password": user1["password"],
        },
    )

    token1 = login1.json()["access_token"]

    # User 2
    user2 = {
        "name": "Alex",
        "email": "alex@example.com",
        "password": "password123",
    }

    client.post("/api/v1/register", json=user2)

    login2 = client.post(
        "/api/v1/login",
        data={
            "username": user2["email"],
            "password": user2["password"],
        },
    )

    token2 = login2.json()["access_token"]

    # User 1 creates two reviews
    client.post(
        "/api/v1/review",
        json={
            "title": "Ved Review 1",
            "rating": 5,
            "feedback": "Excellent.",
        },
        headers={"Authorization": f"Bearer {token1}"},
    )

    client.post(
        "/api/v1/review",
        json={
            "title": "Ved Review 2",
            "rating": 4,
            "feedback": "Pretty good.",
        },
        headers={"Authorization": f"Bearer {token1}"},
    )

    # User 2 creates one review
    client.post(
        "/api/v1/review",
        json={
            "title": "Alex Review",
            "rating": 3,
            "feedback": "Average.",
        },
        headers={"Authorization": f"Bearer {token2}"},
    )

    # User 1 requests their reviews
    response = client.get(
        "/api/v1/me/reviews",
        headers={"Authorization": f"Bearer {token1}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "Ved Review 1"
    assert data[1]["title"] == "Ved Review 2"

def test_get_review(client):
    user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    client.post("/api/v1/register", json=user_data)

    login_response = client.post(
        "/api/v1/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    token = login_response.json()["access_token"]

    create_response = client.post(
        "/api/v1/review",
        json={
            "title": "Great product",
            "rating": 5,
            "feedback": "Really good.",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert create_response.status_code == 201

    review_id = create_response.json()["id"]

    response = client.get(f"/api/v1/reviews/{review_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == review_id
    assert data["title"] == "Great product"
    assert data["rating"] == 5
    assert data["feedback"] == "Really good."

def test_get_review_not_found(client):
    response = client.get("/api/v1/reviews/999999")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Review not found"

def test_update_own_review(client):
    user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    client.post("/api/v1/register", json=user_data)

    login_response = client.post(
        "/api/v1/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/api/v1/review",
        json={
            "title": "Original title",
            "rating": 3,
            "feedback": "Original feedback.",
        },
        headers=headers,
    )

    assert create_response.status_code == 201

    review_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/reviews/{review_id}",
        json={
            "title": "Updated title",
            "rating": 5,
            "feedback": "Updated feedback.",
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == review_id
    assert data["title"] == "Updated title"
    assert data["rating"] == 5
    assert data["feedback"] == "Updated feedback."

def test_cannot_update_another_users_review(client):
    # User 1
    user1 = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    client.post("/api/v1/register", json=user1)

    login1 = client.post(
        "/api/v1/login",
        data={
            "username": user1["email"],
            "password": user1["password"],
        },
    )

    token1 = login1.json()["access_token"]

    # User 2
    user2 = {
        "name": "Alex",
        "email": "alex@example.com",
        "password": "password123",
    }

    client.post("/api/v1/register", json=user2)

    login2 = client.post(
        "/api/v1/login",
        data={
            "username": user2["email"],
            "password": user2["password"],
        },
    )

    token2 = login2.json()["access_token"]

    # User 2 creates the review
    create_response = client.post(
        "/api/v1/review",
        json={
            "title": "Alex's review",
            "rating": 4,
            "feedback": "Alex's feedback.",
        },
        headers={"Authorization": f"Bearer {token2}"},
    )

    assert create_response.status_code == 201

    review_id = create_response.json()["id"]

    # User 1 tries to update User 2's review
    response = client.put(
        f"/api/v1/reviews/{review_id}",
        json={
            "title": "Hacked title",
            "rating": 1,
            "feedback": "Hacked feedback.",
        },
        headers={"Authorization": f"Bearer {token1}"},
    )

    assert response.status_code == 403

    data = response.json()

    assert data["detail"] == "You cannot edit this review"

def test_delete_own_review(client):
    user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    client.post("/api/v1/register", json=user_data)

    login_response = client.post(
        "/api/v1/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/api/v1/review",
        json={
            "title": "Review to delete",
            "rating": 4,
            "feedback": "This will be deleted.",
        },
        headers=headers,
    )

    assert create_response.status_code == 201

    review_id = create_response.json()["id"]

    response = client.delete(
        f"/api/v1/reviews/{review_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Review deleted succesfully"

    # Verify it is actually gone
    get_response = client.get(
        f"/api/v1/reviews/{review_id}"
    )

    assert get_response.status_code == 404

def test_cannot_delete_another_users_review(client):
    # User 1
    user1 = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    client.post("/api/v1/register", json=user1)

    login1 = client.post(
        "/api/v1/login",
        data={
            "username": user1["email"],
            "password": user1["password"],
        },
    )

    token1 = login1.json()["access_token"]

    # User 2
    user2 = {
        "name": "Alex",
        "email": "alex@example.com",
        "password": "password123",
    }

    client.post("/api/v1/register", json=user2)

    login2 = client.post(
        "/api/v1/login",
        data={
            "username": user2["email"],
            "password": user2["password"],
        },
    )

    token2 = login2.json()["access_token"]

    # User 2 creates the review
    create_response = client.post(
        "/api/v1/review",
        json={
            "title": "Alex's review",
            "rating": 4,
            "feedback": "Alex's feedback.",
        },
        headers={"Authorization": f"Bearer {token2}"},
    )

    assert create_response.status_code == 201

    review_id = create_response.json()["id"]

    # User 1 tries to delete User 2's review
    response = client.delete(
        f"/api/v1/reviews/{review_id}",
        headers={"Authorization": f"Bearer {token1}"},
    )

    assert response.status_code == 403

    data = response.json()

    assert data["detail"] == "You cannot delete this review"

    # Verify the review still exists
    get_response = client.get(
        f"/api/v1/reviews/{review_id}"
    )

    assert get_response.status_code == 200

def test_update_review_not_found(client):
    user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    client.post("/api/v1/register", json=user_data)

    login_response = client.post(
        "/api/v1/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    token = login_response.json()["access_token"]

    response = client.put(
        "/api/v1/reviews/999999",
        json={
            "title": "Updated",
            "rating": 5,
            "feedback": "Updated feedback.",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Review not found"

def test_delete_review_not_found(client):
    user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    client.post("/api/v1/register", json=user_data)

    login_response = client.post(
        "/api/v1/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    token = login_response.json()["access_token"]

    response = client.delete(
        "/api/v1/reviews/999999",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Review not found"

def test_get_review_stats(client):
    user_data = {
        "name": "Ved",
        "email": "ved@example.com",
        "password": "password123",
    }

    client.post("/api/v1/register", json=user_data)

    login_response = client.post(
        "/api/v1/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    ratings = [5, 4, 2]

    for i, rating in enumerate(ratings):
        client.post(
            "/api/v1/review",
            json={
                "title": f"Review {i}",
                "rating": rating,
                "feedback": f"Feedback {i}",
            },
            headers=headers,
        )

    response = client.get("/api/v1/reviews/stats")

    assert response.status_code == 200

    data = response.json()

    assert data["total_reviews"] == 3
    assert data["average_rating"] == "3.67"
    assert data["highest_rating"] == 5
    assert data["lowest_rating"] == 2