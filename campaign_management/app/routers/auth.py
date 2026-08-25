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
from app.schemas.response import SuccessResponse
from app.services.auth_service import register_user, login_user, refresh_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED
)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user = register_user(db, user_data.email, user_data.password, user_data.full_name)

    return {
        "success": True,
        "message": "Account registered successfully",
        "data": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
        },
    }


@router.post("/login", response_model=SuccessResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    result = login_user(db, login_data.email, login_data.password)

    return {"success": True, "message": "Login successful", "data": result}


@router.post("/refresh", response_model=SuccessResponse)
def refresh(refresh_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    result = refresh_access_token(db, refresh_data.refresh_token)

    return {
        "success": True,
        "message": "Access token refreshed successfully",
        "data": result,
    }
