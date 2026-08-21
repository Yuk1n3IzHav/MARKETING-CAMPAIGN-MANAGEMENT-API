from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import (
    UserCreate,
    UserResponse,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
)
from app.services.auth_service import (
    register_user,
    login_user,
    refresh_access_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    return register_user(
        db,
        user_data.email,
        user_data.password,
        user_data.full_name,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    return login_user(
        db,
        login_data.email,
        login_data.password,
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    return refresh_access_token(
        db,
        refresh_data.refresh_token,
    )
