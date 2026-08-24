from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.campaign_task import (
    CampaignTaskCreate,
    CampaignTaskUpdate,
)
from app.services import campaign_task_service

router = APIRouter(tags=["Campaign Tasks"])


@router.post(
    "/campaigns/{campaign_id}/campaign-tasks",
    status_code=status.HTTP_201_CREATED,
)
def create_campaign_task(
    campaign_id: int,
    task_data: CampaignTaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = campaign_task_service.create_task(
        db,
        campaign_id,
        current_user.id,
        task_data,
    )

    return {
        "success": True,
        "message": "Campaign task created successfully",
        "data": task,
    }


@router.get("/campaigns/{campaign_id}/campaign-tasks")
def get_campaign_tasks(
    campaign_id: int,
    status: str | None = Query(None),
    priority: str | None = Query(None),
    assignee_id: int | None = Query(None),
    search: str | None = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tasks = campaign_task_service.get_tasks(
        db=db,
        campaign_id=campaign_id,
        user_id=current_user.id,
        status=status,
        priority=priority,
        assignee_id=assignee_id,
        search=search,
        offset=offset,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    return {
        "success": True,
        "message": "Campaign tasks retrieved successfully",
        "data": tasks,
    }


@router.get("/campaign-tasks/{task_id}")
def get_campaign_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = campaign_task_service.get_task_detail(
        db,
        task_id,
        current_user.id,
    )

    return {
        "success": True,
        "message": "Campaign task retrieved successfully",
        "data": task,
    }


@router.patch("/campaign-tasks/{task_id}")
def update_campaign_task(
    task_id: int,
    task_data: CampaignTaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = campaign_task_service.update_task(
        db,
        task_id,
        current_user.id,
        task_data,
    )

    return {
        "success": True,
        "message": "Campaign task updated successfully",
        "data": task,
    }


@router.delete("/campaign-tasks/{task_id}")
def delete_campaign_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    campaign_task_service.delete_task(
        db,
        task_id,
        current_user.id,
    )

    return {
        "success": True,
        "message": "Campaign task deleted successfully",
        "data": None,
    }
