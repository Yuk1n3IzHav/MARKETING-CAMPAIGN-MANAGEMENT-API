from typing import Any

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Any | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    status_code: int
    message: str


class PaginationResponse(BaseModel):
    total: int
    offset: int
    limit: int