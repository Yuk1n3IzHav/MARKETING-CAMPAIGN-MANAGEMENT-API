from db.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer


class CampaignMember(Base):
    __tablename__ = "campaign_members"

    campaign_id = Column(Integer, ForeignKey("campaigns.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(Enum("OWNER", "MEMBER"), nullable=False)

    joined_at = Column(DateTime, default=datetime.now, nullable=False)

    campaign = relationship("Campaign", back_populates="members")

    user = relationship("User", back_populates="campaign_members")
