from datetime import datetime, timedelta

from app.db.database import SessionLocal
from app.models.user import User
from app.models.campaign import Campaign
from app.models.campaign_member import CampaignMember
from app.models.campaign_task import CampaignTask
from app.core.security import hash_password

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
        description="Marketing campaign for the summer season.",
        owner_id=user1.id,
    )

    campaign2 = Campaign(
        name="Product Launch Campaign",
        description="Campaign for launching a new product.",
        owner_id=user2.id,
    )

    db.add_all([campaign1, campaign2])
    db.commit()

    db.refresh(campaign1)
    db.refresh(campaign2)

    # CAMPAIGN MEMBERS

    members = [
        CampaignMember(
            campaign_id=campaign1.id,
            user_id=user1.id,
            role="OWNER",
        ),
        CampaignMember(
            campaign_id=campaign1.id,
            user_id=user2.id,
            role="MEMBER",
        ),
        CampaignMember(
            campaign_id=campaign1.id,
            user_id=admin.id,
            role="MEMBER",
        ),
        CampaignMember(
            campaign_id=campaign2.id,
            user_id=user2.id,
            role="OWNER",
        ),
        CampaignMember(
            campaign_id=campaign2.id,
            user_id=user1.id,
            role="MEMBER",
        ),
    ]

    db.add_all(members)
    db.commit()

    # CAMPAIGN TASKS

    tasks = [
        CampaignTask(
            campaign_id=campaign1.id,
            title="Prepare marketing plan",
            description="Create the overall marketing plan.",
            assignee_id=user1.id,
            status="TODO",
            priority="HIGH",
            due_date=datetime.now() + timedelta(days=7),
        ),
        CampaignTask(
            campaign_id=campaign1.id,
            title="Design social media posts",
            description="Prepare social media content.",
            assignee_id=user2.id,
            status="IN_PROGRESS",
            priority="MEDIUM",
            due_date=datetime.now() + timedelta(days=5),
        ),
        CampaignTask(
            campaign_id=campaign1.id,
            title="Review campaign content",
            description="Review all campaign materials.",
            assignee_id=admin.id,
            status="DONE",
            priority="LOW",
            due_date=datetime.now() + timedelta(days=3),
        ),
        CampaignTask(
            campaign_id=campaign2.id,
            title="Prepare product announcement",
            description="Write the product launch announcement.",
            assignee_id=user2.id,
            status="TODO",
            priority="HIGH",
            due_date=datetime.now() + timedelta(days=10),
        ),
        CampaignTask(
            campaign_id=campaign2.id,
            title="Create launch banner",
            description="Design the main product launch banner.",
            assignee_id=user1.id,
            status="IN_PROGRESS",
            priority="MEDIUM",
            due_date=datetime.now() + timedelta(days=6),
        ),
    ]

    db.add_all(tasks)
    db.commit()

    print("Seed data created successfully.")
    print("Users: 3")
    print("Campaigns: 2")
    print("Campaign members: 5")
    print("Campaign tasks: 5")

except Exception as e:
    db.rollback()
    print(f"Seed failed: {e}")

finally:
    db.close()
