from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.db.database import Base


class CampaignAttachment(Base):
    __tablename__ = "campaign_attachments"

    id = Column(Integer, primary_key=True, autoincrement=True)

    campaign_task_id = Column(Integer, ForeignKey("campaign_tasks.id"), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    file_name = Column(String(255), nullable=False)

    file_path = Column(String(500), nullable=False)

    file_type = Column(String(100), nullable=False)

    file_size = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
