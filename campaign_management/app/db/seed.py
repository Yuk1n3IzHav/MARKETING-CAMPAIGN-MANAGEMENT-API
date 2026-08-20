from datetime import datetime, timedelta

from app.db.database import SessionLocal
from app.core.security import hash_password

from app.models.user import User
from app.models.campaign import Campaign
from app.models.campaign_member import CampaignMember
from app.models.campaign_task import CampaignTask

db = SessionLocal()

try:
    # USERS

    admin = User(
        email="admin@example.com",
        password_hash=hash_password("Admin123"),
        full_name="System Admin",
        role="ADMIN",
        is_active=True,
    )

    user1 = User(
        email="user1@example.com",
        password_hash=hash_password("User123"),
        full_name="Nguyen Van An",
        role="USER",
        is_active=True,
    )

    user2 = User(
        email="user2@example.com",
        password_hash=hash_password("User123"),
        full_name="Tran Thi Binh",
        role="USER",
        is_active=True,
    )

    db.add_all([admin, user1, user2])
    db.commit()

    db.refresh(admin)
    db.refresh(user1)
    db.refresh(user2)

    # CAMPAIGNS

    campaign1 = Campaign(
        name="Summer Marketing Campaign",
        description="Marketing campaign for the summer product launch.",
        owner_id=admin.id,
    )

    campaign2 = Campaign(
        name="Product Launch Campaign",
        description="Campaign for promoting the new product.",
        owner_id=user1.id,
    )

    db.add_all([campaign1, campaign2])
    db.commit()

    db.refresh(campaign1)
    db.refresh(campaign2)

    # CAMPAIGN MEMBERS

    members = [
        CampaignMember(campaign_id=campaign1.id, user_id=admin.id, role="OWNER"),
        CampaignMember(campaign_id=campaign1.id, user_id=user1.id, role="MEMBER"),
        CampaignMember(campaign_id=campaign1.id, user_id=user2.id, role="MEMBER"),
        CampaignMember(campaign_id=campaign2.id, user_id=user1.id, role="OWNER"),
        CampaignMember(campaign_id=campaign2.id, user_id=user2.id, role="MEMBER"),
    ]

    db.add_all(members)
    db.commit()

    # CAMPAIGN TASKS

    tasks = [
        CampaignTask(
            campaign_id=campaign1.id,
            title="Create marketing plan",
            description="Prepare the marketing strategy for the campaign.",
            assignee_id=user1.id,
            status="DONE",
            priority="HIGH",
            due_date=datetime.now() + timedelta(days=2),
        ),
        CampaignTask(
            campaign_id=campaign1.id,
            title="Design social media posts",
            description="Create promotional images for social media.",
            assignee_id=user2.id,
            status="IN_PROGRESS",
            priority="MEDIUM",
            due_date=datetime.now() + timedelta(days=5),
        ),
        CampaignTask(
            campaign_id=campaign1.id,
            title="Launch advertising",
            description="Configure and launch online advertisements.",
            assignee_id=admin.id,
            status="TODO",
            priority="HIGH",
            due_date=datetime.now() + timedelta(days=7),
        ),
        CampaignTask(
            campaign_id=campaign2.id,
            title="Prepare product content",
            description="Write product descriptions and promotional content.",
            assignee_id=user2.id,
            status="IN_PROGRESS",
            priority="MEDIUM",
            due_date=datetime.now() + timedelta(days=4),
        ),
        CampaignTask(
            campaign_id=campaign2.id,
            title="Publish campaign",
            description="Publish the campaign after final approval.",
            assignee_id=user1.id,
            status="TODO",
            priority="HIGH",
            due_date=datetime.now() + timedelta(days=10),
        ),
    ]

    db.add_all(tasks)
    db.commit()

    print("Seed data inserted successfully.")

except Exception as e:
    db.rollback()
    print(f"Seed failed: {e}")

finally:
    db.close()
