from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List
from fastapi.responses import JSONResponse

from services.job import mock_behavior, BackgoundJobClass
from state.instance import BackgroundJobSaver

router = APIRouter(prefix="/job", tags=["Job"])


@router.get("/start", status_code=201)
async def start_normal_behavior():
    print(BackgroundJobSaver.get_instance())

    if BackgroundJobSaver.get_instance() is None:
        bg_job = BackgoundJobClass()
        print(bg_job)
        BackgroundJobSaver.set_instance(bg_job)
        return JSONResponse(
            status_code=201, content={"message": "Background job started."}
        )

    return JSONResponse(
        status_code=409, content={"message": "Background job already running."}
    )


@router.get("/stop", status_code=status.HTTP_200_OK)
async def stop_normal_behavior():
    bg_job = BackgroundJobSaver.get_instance()
    if bg_job is not None:
        if not bg_job.task.done():
            bg_job.task.cancel()
            BackgroundJobSaver.set_instance(None)
            return JSONResponse(
                status_code=200, content={"message": "Background job stopped."}
            )

    return JSONResponse(
        status_code=404, content={"message": "No background job running."}
    )


@router.get("/status", status_code=status.HTTP_200_OK)
async def status_normal_behavior():
    bg_job = BackgroundJobSaver.get_instance()

    return JSONResponse(
        status_code=200,
        content={
            "bg_job_class": str(bg_job),
            "bg_job_task": str(bg_job.task) if bg_job is not None else None,
            "running": bg_job is not None,
        },
    )
