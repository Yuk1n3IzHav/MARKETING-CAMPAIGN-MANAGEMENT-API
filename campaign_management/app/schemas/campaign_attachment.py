from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CampaignAttachmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    campaign_task_id: int
    user_id: int
    file_name: str
    file_path: str
    file_type: str
    file_size: int
    created_at: datetime