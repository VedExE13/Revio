from fastapi import APIRouter,Depends

from app.models.user import User
from app.services.auth_services import get_current_user
from app.schemas.user import UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def me(
    current_user: User = Depends(get_current_user),
):
    return current_user