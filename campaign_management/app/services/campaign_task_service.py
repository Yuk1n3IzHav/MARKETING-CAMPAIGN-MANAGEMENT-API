from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.campaign import Campaign
from app.models.campaign_member import CampaignMember
from app.models.campaign_task import CampaignTask
from app.models.user import User
from app.schemas.campaign_task import CampaignTaskCreate, CampaignTaskUpdate


def get_campaign_member(
    db: Session,
    campaign_id: int,
    user_id: int,
):
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


def get_campaign(
    db: Session,
    campaign_id: int,
):
    campaign = (
        db.query(Campaign)
        .filter(
            Campaign.id == campaign_id,
            Campaign.is_deleted == False,
        )
        .first()
    )

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found",
        )

    return campaign


def get_task(
    db: Session,
    task_id: int,
):
    task = db.query(CampaignTask).filter(CampaignTask.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign task not found",
        )

    return task


def validate_assignee(
    db: Session,
    campaign_id: int,
    assignee_id: int | None,
):
    if assignee_id is None:
        return None

    user = db.query(User).filter(User.id == assignee_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignee not found",
        )

    member = (
        db.query(CampaignMember)
        .filter(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.user_id == assignee_id,
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assignee must be a member of the campaign",
        )

    return user


def create_campaign_task(
    db: Session,
    campaign_id: int,
    user_id: int,
    task_data: CampaignTaskCreate,
):
    get_campaign(db, campaign_id)

    get_campaign_member(
        db,
        campaign_id,
        user_id,
    )

    validate_assignee(
        db,
        campaign_id,
        task_data.assignee_id,
    )

    task = CampaignTask(
        campaign_id=campaign_id,
        title=task_data.title.strip(),
        description=task_data.description,
        due_date=task_data.due_date,
        priority=task_data.priority,
        status=task_data.status,
        assignee_id=task_data.assignee_id,
        created_at=datetime.utcnow(),
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_campaign_tasks(
    db: Session,
    campaign_id: int,
    user_id: int,
    status_value: str | None = None,
    priority: str | None = None,
    assignee_id: int | None = None,
    search: str | None = None,
    offset: int = 0,
    limit: int = 20,
    sort_by: str = "created_at",
):
    get_campaign(db, campaign_id)

    get_campaign_member(
        db,
        campaign_id,
        user_id,
    )

    query = db.query(CampaignTask).filter(CampaignTask.campaign_id == campaign_id)

    if status_value:
        query = query.filter(CampaignTask.status == status_value)

    if priority:
        query = query.filter(CampaignTask.priority == priority)

    if assignee_id:
        query = query.filter(CampaignTask.assignee_id == assignee_id)

    if search:
        query = query.filter(CampaignTask.title.ilike(f"%{search.strip()}%"))

    if sort_by == "due_date":
        query = query.order_by(CampaignTask.due_date.asc())
    else:
        query = query.order_by(CampaignTask.created_at.desc())

    return query.offset(offset).limit(limit).all()


def get_campaign_task(
    db: Session,
    task_id: int,
    user_id: int,
):
    task = get_task(db, task_id)

    get_campaign_member(
        db,
        task.campaign_id,
        user_id,
    )

    return task


def update_campaign_task(
    db: Session,
    task_id: int,
    user_id: int,
    task_data: CampaignTaskUpdate,
):
    task = get_task(db, task_id)

    member = get_campaign_member(
        db,
        task.campaign_id,
        user_id,
    )

    if member.role != "OWNER" and task.assignee_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this task",
        )

    update_data = task_data.model_dump(exclude_unset=True)

    if not update_data:
        return task

    if "title" in update_data:
        if update_data["title"] is not None:
            update_data["title"] = update_data["title"].strip()

            if not update_data["title"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Task title cannot be empty",
                )

    if "assignee_id" in update_data:
        validate_assignee(
            db,
            task.campaign_id,
            update_data["assignee_id"],
        )

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


def delete_campaign_task(
    db: Session,
    task_id: int,
    user_id: int,
):
    task = get_task(db, task_id)

    member = get_campaign_member(
        db,
        task.campaign_id,
        user_id,
    )

    # Owner mới được xóa task
    if member.role != "OWNER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only campaign owner can delete a task",
        )

    db.delete(task)
    db.commit()

    return {"message": "Campaign task deleted successfully"}
