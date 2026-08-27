from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class CampaignComment(Base):
    __tablename__ = "campaign_comments"

    id = Column(Integer, primary_key=True, autoincrement=True)

    campaign_task_id = Column(Integer, ForeignKey("campaign_tasks.id"), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    content = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.now, nullable=False)

    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    campaign_task = relationship("CampaignTask", back_populates="comments")

    user = relationship("User", back_populates="campaign_comments")
