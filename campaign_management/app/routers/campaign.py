from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.campaign import (
    CampaignCreate,
    CampaignUpdate,
    CampaignResponse,
    CampaignMemberResponse,
)
from app.schemas.campaign_member import (
    CampaignMemberCreate,
)
from app.services.campaign_service import (
    create_campaign,
    get_campaigns,
    get_campaign_detail,
    update_campaign,
    delete_campaign,
)
from app.services.campaign_member_service import (
    add_member,
    remove_member,
    get_campaign_members,
)

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_campaign(
    campaign_data: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    campaign = create_campaign(db, current_user.id, campaign_data)

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


@router.get("")
def get_campaigns(
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    campaigns = get_campaigns(db, current_user.id, search)

    data = []

    for campaign in campaigns:
        data.append(
            {
                "id": campaign.id,
                "name": campaign.name,
                "description": campaign.description,
                "role": campaign.role,
            }
        )

    return {
        "success": True,
        "message": "Campaigns retrieved successfully",
        "data": data,
    }


@router.get(
    "/{campaign_id}",
    response_model=CampaignResponse,
)
def get_detail(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_campaign_detail(
        db,
        campaign_id,
        current_user,
    )


@router.put(
    "/{campaign_id}",
    response_model=CampaignResponse,
)
def update(
    campaign_id: int,
    data: CampaignUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_campaign(
        db,
        campaign_id,
        current_user,
        data,
    )


@router.patch(
    "/{campaign_id}",
    response_model=CampaignResponse,
)
def patch(
    campaign_id: int,
    data: CampaignUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_campaign(
        db,
        campaign_id,
        current_user,
        data,
    )


@router.delete(
    "/{campaign_id}",
)
def delete(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    delete_campaign(
        db,
        campaign_id,
        current_user,
    )

    return {
        "success": True,
        "message": "Campaign deleted successfully",
        "data": None,
    }


@router.post(
    "/{campaign_id}/members",
    response_model=CampaignMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_campaign_member(
    campaign_id: int,
    data: CampaignMemberCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    member = add_member(
        db,
        campaign_id,
        current_user,
        data.user_id,
    )
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
)
def delete_campaign_member(
    campaign_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    remove_member(db, campaign_id, current_user, user_id)
    return {
        "success": True,
        "message": "Member removed from campaign successfully",
        "data": None,
    }


@router.get(
    "/{campaign_id}/members",
    response_model=list[CampaignMemberResponse],
)
def list_campaign_members(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    members = get_campaign_members(
        db,
        campaign_id,
        current_user,
    )

    return {
        "success": True,
        "message": "Campaign members retrieved successfully",
        "data": [
            {
                "user_id": member.user_id,
                "full_name": member.user.full_name,
                "email": member.user.email,
                "role": member.role,
            }
            for member in members
        ],
    }
