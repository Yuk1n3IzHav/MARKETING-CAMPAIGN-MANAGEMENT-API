from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CampaignMemberCreate(BaseModel):
    user_id: int


class CampaignMemberResponse(BaseModel):
    campaign_id: int
    user_id: int
    email: str
    full_name: str
    role: str
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)