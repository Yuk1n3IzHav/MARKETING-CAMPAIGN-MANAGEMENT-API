from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CampaignBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None


class CampaignResponse(CampaignBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class CampaignMemberResponse(BaseModel):
    campaign_id: int
    user_id: int
    email: str
    full_name: str
    role: str
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)