from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session

from app.models.user import User
from app.db.database import get_db
from app.services.auth_services import get_current_user
from app.schemas.review import ReviewResponse
from app.schemas.review import ReviewCreate
from app.schemas.review import ReviewUpdate
from app.schemas.review import MessageResponse
from app.services.review_services import create_review
from app.services.review_services import get_reviews
from app.services.review_services import get_review
from app.services.review_services import update_review
from app.services.review_services import delete_review


router = APIRouter()

@router.post("/review", response_model=ReviewResponse,status_code=status.HTTP_201_CREATED)
def create_review_route(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_review(db,review_data,current_user)

@router.get("/reviews",response_model=list[ReviewResponse])
def get_reviews_route(
    db: Session = Depends(get_db)
):
    return get_reviews(db)

@router.get("/reviews/{id}",response_model=ReviewResponse)
def get_review_route(
    id: int,
    db: Session = Depends(get_db),
):
    return get_review(db,id)

@router.put("/reviews/{review_id}",response_model=ReviewResponse)
def update_review_route(
    review_id: int,
    review_data: ReviewUpdate,
    db:  Session = Depends(get_db),
    current_user: User = Depends(get_current_user),

):
    return update_review(db,review_id,review_data,current_user,)

@router.delete("/reviews/{review_id}",response_model=MessageResponse)
def delete_review_route(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    
):
    return delete_review(
        db=db,
        review_id=review_id,
        current_user=current_user,
)