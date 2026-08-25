from app.db.database import Base, engine

from app.models.user import User
from app.models.campaign import Campaign
from app.models.campaign_member import CampaignMember
from app.models.campaign_task import CampaignTask


Base.metadata.create_all(bind=engine)

print("Database initialized successfully.")