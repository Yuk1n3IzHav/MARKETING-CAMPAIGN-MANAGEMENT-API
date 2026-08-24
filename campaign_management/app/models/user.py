from app.db.database import Base
from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum("USER", "ADMIN"), nullable=False, default="USER")
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    owned_campaigns = relationship("Campaign", back_populates="owner")

    campaign_members = relationship("CampaignMember", back_populates="user")

    campaign_tasks = relationship("CampaignTask", back_populates="assignee")

    campaign_audit_logs = relationship("CampaignAuditLog", back_populates="user")
