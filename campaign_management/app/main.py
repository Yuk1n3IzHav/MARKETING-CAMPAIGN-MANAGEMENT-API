from fastapi import FastAPI

from app.utils.exceptions import register_exception_handlers

from app.routers import auth
from app.routers import users
from app.routers import campaign
from app.routers import campaign_task

app = FastAPI(title="Campaign Management API", version="1.0.0")


register_exception_handlers(app)


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

app.include_router(users.router, prefix="/users", tags=["Users"])

app.include_router(campaign.router, prefix="/campaigns", tags=["Campaigns"])

app.include_router(
    campaign_task.router, prefix="/campaign-tasks", tags=["Campaign Tasks"]
)


@app.get("/health")
def health_check():
    return {"success": True, "message": "API is running"}
