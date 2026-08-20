from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class CampaignMemberBase(BaseModel):
    campaign_id: int
    user_id: int
    role: Literal["OWNER", "MEMBER"]


class CampaignMemberCreate(CampaignMemberBase):
    pass


class CampaignMemberUpdate(BaseModel):
    role: Literal["OWNER", "MEMBER"] | None = None


class CampaignMemberResponse(CampaignMemberBase):
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)