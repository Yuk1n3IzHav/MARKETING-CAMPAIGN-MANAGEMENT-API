from fastapi import FastAPI

from app.utils.exceptions import register_exception_handlers
from app.routers import auth, users, campaign, campaign_task

app = FastAPI(title="Campaign Management API", version="1.0.0")

register_exception_handlers(app)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(campaign.router)
app.include_router(campaign_task.router)


@app.get("/health")
def health_check():
    return {"success": True, "message": "API is running"}
