from app.db.database import Base
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Enum, Text
from sqlalchemy.orm import relationship


class CampaignTask(Base):
    __tablename__ = "campaign_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(Enum("TODO", "IN_PROGRESS", "DONE"), default="TODO", nullable=False)
    priority = Column(Enum("LOW", "MEDIUM", "HIGH"), default="MEDIUM", nullable=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    campaign = relationship("Campaign", back_populates="tasks")

    assignee = relationship("User", back_populates="assigned_tasks")

    comments = relationship(
        "CampaignComment", back_populates="campaign_task", cascade="all, delete-orphan"
    )
