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


@router.post(
    "",
    response_model=CampaignResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    data: CampaignCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_campaign(
        db,
        current_user,
        data,
    )


@router.get(
    "",
    response_model=list[CampaignResponse],
)
def get_list(
    search: str | None = Query(
        default=None,
        max_length=255,
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_campaigns(
        db,
        current_user,
        search,
    )


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
    return delete_campaign(
        db,
        campaign_id,
        current_user,
    )


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
    return add_member(
        db,
        campaign_id,
        current_user,
        data.user_id,
    )


@router.delete(
    "/{campaign_id}/members/{user_id}",
)
def delete_campaign_member(
    campaign_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return remove_member(
        db,
        campaign_id,
        current_user,
        user_id,
    )


@router.get(
    "/{campaign_id}/members",
    response_model=list[CampaignMemberResponse],
)
def list_campaign_members(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_campaign_members(
        db,
        campaign_id,
        current_user,
    )
