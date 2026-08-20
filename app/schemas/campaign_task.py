from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class CampaignTaskBase(BaseModel):
    title: str
    description: str | None = None
    assignee_id: int | None = None
    status: Literal["TODO", "IN_PROGRESS", "DONE"] = "TODO"
    priority: Literal["LOW", "MEDIUM", "HIGH"] = "MEDIUM"
    due_date: datetime | None = None


class CampaignTaskCreate(CampaignTaskBase):
    campaign_id: int


class CampaignTaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    assignee_id: int | None = None
    status: Literal["TODO", "IN_PROGRESS", "DONE"] | None = None
    priority: Literal["LOW", "MEDIUM", "HIGH"] | None = None
    due_date: datetime | None = None


class CampaignTaskResponse(CampaignTaskBase):
    id: int
    campaign_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)