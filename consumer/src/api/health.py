from fastapi import APIRouter, status, BackgroundTasks
from services.log import LoggingBackgroundClass

router = APIRouter(prefix="", tags=["Health"])


@router.get("/", status_code=status.HTTP_200_OK)
async def health(backgound_tasks: BackgroundTasks):
    LoggingBackgroundClass()
    return {"health": "ok"}
