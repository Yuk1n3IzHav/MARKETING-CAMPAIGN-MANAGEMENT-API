from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.campaign_comment import CampaignComment
from app.models.campaign_task import CampaignTask
from app.models.campaign_member import CampaignMember
from app.schemas.campaign_comment import CampaignCommentCreate


def get_task(db: Session, task_id: int):
    task = db.query(CampaignTask).filter(CampaignTask.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign task not found",
        )

    return task


def check_campaign_member(db: Session, campaign_id: int, user_id: int):
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


def create_comment(
    db: Session, task_id: int, user_id: int, data: CampaignCommentCreate
):
    task = get_task(db, task_id)

    check_campaign_member(db, task.campaign_id, user_id)

    content = data.content.strip()

    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Comment cannot be empty",
        )

    comment = CampaignComment(
        campaign_task_id=task.id, user_id=user_id, content=content
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


def get_comments(db: Session, task_id: int, user_id: int):
    task = get_task(db, task_id)

    check_campaign_member(db, task.campaign_id, user_id)

    return (
        db.query(CampaignComment)
        .filter(CampaignComment.campaign_task_id == task_id)
        .order_by(CampaignComment.created_at.asc())
        .all()
    )
