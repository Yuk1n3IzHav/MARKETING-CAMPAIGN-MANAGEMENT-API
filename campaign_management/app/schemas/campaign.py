from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CampaignCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None


class CampaignUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None


class CampaignCreateResponse(BaseModel):
    id: int
    name: str
    description: str | None
    role: str


class CampaignResponse(BaseModel):
    id: int
    name: str
    description: str | None
    role: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CampaignMemberResponse(BaseModel):
    user_id: int
    full_name: str
    email: str
    role: str


class CampaignMemberCreateResponse(BaseModel):
    user_id: int
    campaign_id: int
    role: str