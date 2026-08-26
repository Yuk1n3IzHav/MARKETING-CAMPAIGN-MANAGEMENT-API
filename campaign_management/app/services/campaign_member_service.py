from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.campaign import Campaign
from app.models.campaign_member import CampaignMember
from app.models.user import User
from app.models.campaign_audit_log import CampaignAuditLog


def _get_campaign(db: Session, campaign_id: int):
    campaign = (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id, Campaign.is_deleted == False)
        .first()
    )

    if campaign is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found"
        )

    return campaign


def _check_owner(campaign: Campaign, current_user: User):
    if campaign.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the campaign owner can manage members",
        )


def _create_audit_log(db: Session, campaign_id: int, user_id: int, action: str):
    if CampaignAuditLog is None:
        return

    log = CampaignAuditLog(campaign_id=campaign_id, user_id=user_id, action=action)

    db.add(log)


def add_member(db: Session, campaign_id: int, current_user: User, user_id: int):
    campaign = _get_campaign(db, campaign_id)

    _check_owner(campaign, current_user)

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot add an inactive user",
        )

    existing_member = (
        db.query(CampaignMember)
        .filter(
            CampaignMember.campaign_id == campaign_id, CampaignMember.user_id == user_id
        )
        .first()
    )

    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this campaign",
        )

    member = CampaignMember(campaign_id=campaign_id, user_id=user_id, role="MEMBER")

    db.add(member)

    _create_audit_log(db, campaign_id, current_user.id, "ADD_MEMBER")

    db.commit()
    db.refresh(member)

    return member


def remove_member(db: Session, campaign_id: int, current_user: User, user_id: int):
    campaign = _get_campaign(db, campaign_id)

    _check_owner(campaign, current_user)

    member = (
        db.query(CampaignMember)
        .filter(
            CampaignMember.campaign_id == campaign_id, CampaignMember.user_id == user_id
        )
        .first()
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Campaign member not found"
        )

    if member.role == "OWNER":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The campaign owner cannot be removed",
        )

    db.delete(member)

    _create_audit_log(db, campaign_id, current_user.id, "REMOVE_MEMBER")

    db.commit()

    return {"success": True, "message": "Member removed successfully"}


def get_campaign_members(db: Session, campaign_id: int, current_user: User):
    campaign = _get_campaign(db, campaign_id)

    member = (
        db.query(CampaignMember)
        .filter(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.user_id == current_user.id,
        )
        .first()
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this campaign",
        )

    members = (
        db.query(CampaignMember)
        .join(User, User.id == CampaignMember.user_id)
        .filter(CampaignMember.campaign_id == campaign_id)
        .order_by(CampaignMember.joined_at.asc())
        .all()
    )

    return members
