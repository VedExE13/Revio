from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate
from app.services.user_service import create_user
from app.schemas.user import UserResponse

router = APIRouter()

@router.post("/register",status_code=status.HTTP_201_CREATED,response_model=UserResponse,)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    return create_user(db, user_data)