from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user, require_admin
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.user_service import get_users

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("", response_model=list[UserResponse])
def get_all_users(
    search: str | None = Query(default=None),
    is_active: bool | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_users(db, search, is_active)
