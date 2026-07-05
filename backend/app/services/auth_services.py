from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends




from app.core.security import verify_password
from app.models.user import User
from app.schemas.user import UserLogin
from app.core.security import decode_access_token
from app.core.security import oauth2_scheme
from app.db.session import get_db


def authenticate_user(
    db: Session,
    user_data: UserLogin,
):

    exist_user = (
        db.query(User)
        .filter(User.email == user_data.email) 
        .first()
)
    if not exist_user:
        raise HTTPException(
    status_code=401,
    detail="Invalid email or password",
    )



    if not verify_password(
    user_data.password,
    exist_user.hashed_password,
    
):
        raise HTTPException(
        status_code=401,
        detail="Invalid email or password",
    )
    return exist_user


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    user_id = decode_access_token(token)

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    return user
