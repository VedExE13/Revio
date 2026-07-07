from sqlalchemy.orm import Session

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