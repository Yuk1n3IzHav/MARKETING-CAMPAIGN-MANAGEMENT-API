from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CampaignCommentCreate(BaseModel):
    content: str


class CampaignCommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    campaign_task_id: int
    user_id: int
    content: str
    created_at: datetime
    updated_at: datetime