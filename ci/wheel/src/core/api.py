from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from core.config import get_settings
from core.service import create_runner
from core.schema import AuthRequest


settings = get_settings()

webhook_router = APIRouter(
    prefix="/webhooks",
    tags=["webhooks"],
)


def auth_middleware(auth: AuthRequest):
    if auth.token != settings.github_webhook_secret:
        raise HTTPException(status_code=403, detail="Invalid token")

    return auth


@webhook_router.post("/github/service/{service_name}", status_code=200)
async def github_webhook(
    service_name: str, bg: BackgroundTasks, auth: AuthRequest = Depends(auth_middleware)
):
    bg.add_task(create_runner, service_name)
    return {"service_name": service_name}
