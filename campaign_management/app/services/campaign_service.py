from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.campaign import Campaign
from app.models.campaign_member import CampaignMember
from app.models.user import User
from app.models.campaign_audit_log import CampaignAuditLog
from app.schemas.campaign import CampaignCreate, CampaignUpdate


def _validate_campaign_name(name: str) -> str:
    name = name.strip()

    if not name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Campaign name cannot be empty",
        )

    if len(name) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Campaign name cannot exceed 255 characters",
        )

    return name


def _get_campaign(db: Session, campaign_id: int):
    campaign = (
        db.query(Campaign)
        .filter(
            Campaign.id == campaign_id,
            Campaign.is_deleted == False,
        )
        .first()
    )

    if campaign is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found",
        )

    return campaign


def _check_member(db: Session, campaign_id: int, user_id: int):
    member = (
        db.query(CampaignMember)
        .filter(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.user_id == user_id,
        )
        .first()
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this campaign",
        )

    return member


def _check_owner(campaign: Campaign, user: User):
    if campaign.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the campaign owner can perform this action",
        )


def _create_audit_log(db: Session, campaign_id: int, user_id: int, action: str):
    log = CampaignAuditLog(
        campaign_id=campaign_id,
        user_id=user_id,
        action=action,
    )
    db.add(log)


def create_campaign(db: Session, current_user: User, data: CampaignCreate):
    name = _validate_campaign_name(data.name)

    campaign = Campaign(
        name=name,
        description=data.description,
        owner_id=current_user.id,
    )

    db.add(campaign)
    db.flush()

    owner_member = CampaignMember(
        campaign_id=campaign.id,
        user_id=current_user.id,
        role="OWNER",
    )

    db.add(owner_member)
    _create_audit_log(db, campaign.id, current_user.id, "CREATE_CAMPAIGN")

    db.commit()
    db.refresh(campaign)

    return campaign


def get_campaigns(
    db: Session,
    current_user: User,
    search: str | None = None,
):
    query = (
        db.query(Campaign, CampaignMember.role)
        .join(
            CampaignMember,
            CampaignMember.campaign_id == Campaign.id,
        )
        .filter(
            CampaignMember.user_id == current_user.id,
            Campaign.is_deleted == False,
        )
    )

    if search:
        search = search.strip()

        if search:
            query = query.filter(Campaign.name.ilike(f"%{search}%"))

    return query.order_by(Campaign.created_at.desc()).all()


def get_campaign_detail(
    db: Session,
    campaign_id: int,
    current_user: User,
):
    campaign = _get_campaign(db, campaign_id)
    _check_member(db, campaign.id, current_user.id)
    return campaign


def update_campaign(
    db: Session,
    campaign_id: int,
    current_user: User,
    data: CampaignUpdate,
):
    campaign = _get_campaign(db, campaign_id)
    _check_owner(campaign, current_user)

    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data to update",
        )

    if "name" in update_data and update_data["name"] is not None:
        update_data["name"] = _validate_campaign_name(update_data["name"])

    for field, value in update_data.items():
        setattr(campaign, field, value)

    _create_audit_log(
        db,
        campaign.id,
        current_user.id,
        "UPDATE_CAMPAIGN",
    )

    db.commit()
    db.refresh(campaign)

    return campaign


def delete_campaign(
    db: Session,
    campaign_id: int,
    current_user: User,
):
    campaign = _get_campaign(db, campaign_id)
    _check_owner(campaign, current_user)

    from datetime import datetime

    campaign.is_deleted = True
    campaign.deleted_at = datetime.now()

    _create_audit_log(
        db,
        campaign.id,
        current_user.id,
        "DELETE_CAMPAIGN",
    )

    db.commit()

    return campaign
