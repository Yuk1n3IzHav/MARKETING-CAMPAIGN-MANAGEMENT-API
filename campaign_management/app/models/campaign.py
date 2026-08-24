from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(255), nullable=False)

    description = Column(Text, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.now, nullable=False)

    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=True
    )

    is_deleted = Column(Boolean, default=False, nullable=False)

    deleted_at = Column(DateTime, nullable=True)

    owner = relationship("User", back_populates="owned_campaigns")

    members = relationship("CampaignMember", back_populates="campaign")

    tasks = relationship("CampaignTask", back_populates="campaign")
