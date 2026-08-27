from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CampaignTaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    due_date: datetime | None = None

    priority: Literal["LOW", "MEDIUM", "HIGH"] = "MEDIUM"

    status: Literal["TODO", "IN_PROGRESS", "DONE"] = "TODO"

    assignee_id: int | None = None


class CampaignTaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    due_date: datetime | None = None

    priority: Literal["LOW", "MEDIUM", "HIGH"] = "MEDIUM"

    assignee_id: int | None = None


class CampaignTaskUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    due_date: datetime | None = None

    priority: Literal["LOW", "MEDIUM", "HIGH"] | None = None

    status: Literal["TODO", "IN_PROGRESS", "DONE"] | None = None

    assignee_id: int | None = None


class CampaignTaskResponse(CampaignTaskBase):
    id: int
    campaign_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
