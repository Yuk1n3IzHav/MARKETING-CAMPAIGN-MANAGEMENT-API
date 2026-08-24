from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class CampaignAuditLog(Base):
    __tablename__ = "campaign_audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)

    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    action = Column(String(50), nullable=False)

    created_at = Column(DateTime, default=datetime.now, nullable=False)

    campaign = relationship("Campaign")

    user = relationship("User")
