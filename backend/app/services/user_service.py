from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate
from fastapi import HTTPException



def create_user(
    db: Session,
    user_data: UserCreate,


):
    existing_user = (
    db.query(User)
    .filter(User.email == user_data.email)
    .first()
)
    if existing_user:
        raise HTTPException(
             status_code=409,
             detail="Email already registered",
        )
    hashed_password = hash_password(user_data.password)
    user = User(
        name = user_data.name,
        email = user_data.email,
        hashed_password = hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

