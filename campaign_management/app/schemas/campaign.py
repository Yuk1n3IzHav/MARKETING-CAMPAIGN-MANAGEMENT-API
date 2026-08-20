from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CampaignBase(BaseModel):
    name: str
    description: str | None = None


class CampaignCreate(CampaignBase):
    owner_id: int


class CampaignUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class CampaignResponse(CampaignBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)