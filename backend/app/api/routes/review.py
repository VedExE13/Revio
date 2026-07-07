from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session

from app.models.user import User
from app.db.database import get_db
from app.services.auth_services import get_current_user
from app.schemas.review import ReviewResponse
from app.schemas.review import ReviewCreate
from app.services.review_services import create_review

router = APIRouter()

@router.post("/reviews", response_model=ReviewResponse,status_code=status.HTTP_201_CREATED)
def create_review_route(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_review(db,review_data,current_user)