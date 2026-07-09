from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db.database import get_db
from app.schemas.user import UserCreate
from app.schemas.user import UserLogin
from app.services.user_service import create_user
from app.schemas.user import UserResponse
from app.schemas.user import Token
from app.services.auth_services import authenticate_user
from app.core.security import create_access_token

router = APIRouter()

@router.post("/register",status_code=status.HTTP_201_CREATED,response_model=UserResponse,)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    return create_user(db, user_data)

@router.post("/login",status_code=status.HTTP_200_OK,response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    
):
    user_data = UserLogin(
    email=form_data.username,
    password=form_data.password,
)
    user = authenticate_user(db,user_data,)
    access_token = create_access_token(
        data={
            "sub": str(user.id)
        }
    )
    return {
    "access_token": access_token,
    "token_type": "bearer",
}

