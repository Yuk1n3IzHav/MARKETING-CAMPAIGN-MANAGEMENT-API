from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user, require_admin
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("", response_model=list[UserResponse])
def get_users(current_user: User = Depends(require_admin)):
    return []
