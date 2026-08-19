from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    id: int
    role: Literal["USER", "ADMIN"]
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)