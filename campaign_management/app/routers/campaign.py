from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.campaign import (
    CampaignCreate,
    CampaignUpdate,
)
from app.schemas.campaign_member import CampaignMemberCreate
from app.schemas.response import SuccessResponse

from app.services.campaign_service import (
    create_campaign as create_campaign_service,
    get_campaigns as get_campaigns_service,
    get_campaign_detail,
    update_campaign as update_campaign_service,
    delete_campaign as delete_campaign_service,
)

from app.services.campaign_member_service import (
    add_member as add_member_service,
    remove_member as remove_member_service,
    get_campaign_members as get_campaign_members_service,
)

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


@router.post("", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_campaign(
    campaign_data: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    campaign = create_campaign_service(db, current_user.id, campaign_data)

    return {
        "success": True,
        "message": "Campaign created successfully",
        "data": {
            "id": campaign.id,
            "name": campaign.name,
            "description": campaign.description,
            "role": "OWNER",
        },
    }


@router.get("", response_model=SuccessResponse)
def get_campaigns(
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    campaigns = get_campaigns_service(db, current_user.id, search)

    data = [
        {
            "id": campaign.id,
            "name": campaign.name,
            "description": campaign.description,
            "role": campaign.role,
        }
        for campaign in campaigns
    ]

    return {
        "success": True,
        "message": "Campaigns retrieved successfully",
        "data": data,
    }


@router.get("/{campaign_id}", response_model=SuccessResponse)
def get_detail(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    campaign = get_campaign_detail(db, campaign_id, current_user)

    return {
        "success": True,
        "message": "Campaign retrieved successfully",
        "data": campaign,
    }


@router.put("/{campaign_id}", response_model=SuccessResponse)
def update(
    campaign_id: int,
    data: CampaignUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    campaign = update_campaign_service(db, campaign_id, current_user, data)

    return {
        "success": True,
        "message": "Campaign updated successfully",
        "data": campaign,
    }


@router.patch("/{campaign_id}", response_model=SuccessResponse)
def patch(
    campaign_id: int,
    data: CampaignUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    campaign = update_campaign_service(db, campaign_id, current_user, data)

    return {
        "success": True,
        "message": "Campaign updated successfully",
        "data": campaign,
    }


@router.delete("/{campaign_id}", response_model=SuccessResponse)
def delete(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    delete_campaign_service(db, campaign_id, current_user)

    return {"success": True, "message": "Campaign deleted successfully", "data": None}


@router.post(
    "/{campaign_id}/members",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_campaign_member(
    campaign_id: int,
    data: CampaignMemberCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    member = add_member_service(db, campaign_id, current_user, data.user_id)

    return {
        "success": True,
        "message": "Member added to campaign successfully",
        "data": {
            "user_id": member.user_id,
            "campaign_id": member.campaign_id,
            "role": member.role,
        },
    }


@router.delete(
    "/{campaign_id}/members/{user_id}",
    response_model=SuccessResponse,
)
def delete_campaign_member(
    campaign_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    remove_member_service(db, campaign_id, current_user, user_id)

    return {
        "success": True,
        "message": "Member removed from campaign successfully",
        "data": None,
    }


@router.get("/{campaign_id}/members", response_model=SuccessResponse)
def list_campaign_members(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    members = get_campaign_members_service(db, campaign_id, current_user)

    data = [
        {
            "user_id": member.user_id,
            "full_name": member.user.full_name,
            "email": member.user.email,
            "role": member.role,
        }
        for member in members
    ]

    return {
        "success": True,
        "message": "Campaign members retrieved successfully",
        "data": data,
    }
