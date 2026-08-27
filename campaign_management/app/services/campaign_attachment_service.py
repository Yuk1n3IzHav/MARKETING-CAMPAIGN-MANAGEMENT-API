import os
import uuid

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.campaign_attachment import CampaignAttachment
from app.models.campaign_member import CampaignMember
from app.models.campaign_task import CampaignTask

UPLOAD_DIR = "uploads/campaign_tasks"

ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "application/pdf",
}

MAX_FILE_SIZE = 10 * 1024 * 1024


def check_member(db: Session, campaign_id: int, user_id: int):
    member = (
        db.query(CampaignMember)
        .filter(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.user_id == user_id,
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this campaign",
        )

    return member


def upload_attachment(db: Session, task_id: int, user_id: int, file: UploadFile):
    task = db.query(CampaignTask).filter(CampaignTask.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign task not found",
        )

    check_member(db, task.campaign_id, user_id)

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type is not allowed",
        )

    file_data = file.file.read()

    if len(file_data) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must not exceed 10MB",
        )

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    extension = os.path.splitext(file.filename or "")[1]

    file_name = f"{uuid.uuid4()}{extension}"

    file_path = os.path.join(
        UPLOAD_DIR,
        file_name,
    )

    with open(file_path, "wb") as output:
        output.write(file_data)

    attachment = CampaignAttachment(
        campaign_task_id=task.id,
        user_id=user_id,
        file_name=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        file_size=len(file_data),
    )

    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    return attachment
