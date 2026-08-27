from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.campaign_comment import (
    CampaignCommentCreate,
    CampaignCommentResponse,
)
from app.schemas.response import SuccessResponse
from app.services.campaign_comment_service import (
    create_comment,
    get_comments,
)

router = APIRouter(
    prefix="/campaign-tasks",
    tags=["Campaign Task Comments"],
)


@router.post(
    "/{task_id}/comments",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create task comment",
)
def add_comment(
    task_id: int,
    data: CampaignCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = create_comment(db, task_id, current_user.id, data)

    return {
        "success": True,
        "message": "Comment created successfully",
        "data": comment,
    }


@router.get(
    "/{task_id}/comments",
    response_model=SuccessResponse,
    summary="Get task comments",
)
def list_comments(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comments = get_comments(db, task_id, current_user.id)

    return {
        "success": True,
        "message": "Comments retrieved successfully",
        "data": comments,
    }
