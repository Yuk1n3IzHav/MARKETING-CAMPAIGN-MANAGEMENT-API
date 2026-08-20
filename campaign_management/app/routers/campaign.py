from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_campaigns():
    pass


@router.get("/{campaign_id}")
def get_campaign(campaign_id: int):
    pass


@router.post("/")
def create_campaign():
    pass


@router.put("/{campaign_id}")
def update_campaign(campaign_id: int):
    pass


@router.delete("/{campaign_id}")
def delete_campaign(campaign_id: int):
    pass
