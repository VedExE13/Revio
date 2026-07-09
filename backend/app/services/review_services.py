from sqlalchemy.orm import Session
from fastapi import HTTPException


from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewCreate

def create_review(
        db: Session,
        review_data : ReviewCreate,
        current_user: User
):
    review = Review(
        user_id = current_user.id,
        title = review_data.title,
        rating = review_data.rating,
        feedback = review_data.feedback,
)

    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def get_reviews(
    db: Session
):
    reviews = (
    db.query(Review)
    .all()
)

    return reviews

def get_review(
        db: Session,
        id: int,
):
    review = (
    db.query(Review)
    .filter(Review.id == id)
    .first()
)
    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review not found",
        )
    return review