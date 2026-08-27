from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.response import SuccessResponse
from app.services.campaign_attachment_service import upload_attachment


router = APIRouter(
    prefix="/campaign-tasks",
    tags=["Campaign Task Attachments"],
)


@router.post(
    "/{task_id}/attachments",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload task attachment",
)
def upload_task_attachment(
    task_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    attachment = upload_attachment(
        db,
        task_id,
        current_user.id,
        file,
    )

    return {
        "success": True,
        "message": "File uploaded successfully",
        "data": {
            "id": attachment.id,
            "file_name": attachment.file_name,
            "file_path": attachment.file_path,
            "file_type": attachment.file_type,
            "file_size": attachment.file_size,
        },
    }