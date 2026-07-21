from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from decimal import Decimal

from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewCreate
from app.schemas.review import ReviewUpdate
from app.schemas.review import SortOption



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
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: str | None = None,
    sort: SortOption | None = None,
):
    query = db.query(Review)
    if search:
        query = query.filter(
            Review.title.ilike(f"%{search}%")
        )
    if sort == SortOption.newest:
        query = query.order_by(
            Review.created_at.desc()
        )
    elif sort == SortOption.oldest:
        query = query.order_by(
            Review.created_at.asc()
        )
        
    reviews = (
    query
    .offset(skip)
    .limit(limit)
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

def update_review(
        db: Session,
        id: int,
        review_data: ReviewUpdate,
        current_user: User

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
    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot edit this review"
    )
    review.title = review_data.title
    review.rating = review_data.rating
    review.feedback = review_data.feedback
    db.commit()
    db.refresh(review)


  
    return review

def delete_review(
    db: Session,
    review_id: int,
    current_user: User,
):
    review = (
        db.query(Review)
        .filter(Review.id == review_id)
        .first()

    )
    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review not found",
    ) 
    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot delete this review"
    )
    db.delete(review)
    db.commit()

    return {
        "message": "Review deleted succesfully"
    }

def get_my_review(
        db: Session,
        current_user: User,
):
    reviews = (
        db.query(Review)
        .filter(Review.user_id == current_user.id)
        .all()
    )
    return reviews

def get_review_stats(
    db: Session,
):
    review_stats = (
        db.query(
            func.count(Review.id).label("total_reviews"),
            func.avg(Review.rating).label("average_rating"),
            func.max(Review.rating).label("highest_rating"),
            func.min(Review.rating).label("lowest_rating"),
        )
        .first()
    )

    return {
        "total_reviews": review_stats.total_reviews,
        "average_rating": round(float(review_stats.average_rating or 0),2),
        "highest_rating": review_stats.highest_rating or 0,
        "lowest_rating": review_stats.lowest_rating or 0,
    }