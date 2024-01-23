from fastapi import APIRouter, status, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List

from services.full import create_full_cpu_process, create_full_rem_process
from services.job import enqueue as enqueue_task


router = APIRouter(
    prefix="/full",
    tags=["Full"],
)


@router.get("/cpu/duration/{duration}", status_code=status.HTTP_200_OK)
async def full_cpu(duration: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(create_full_cpu_process, duration)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "full_type": "cpu",
            "duration": duration,
            "message": f"full cpu in {duration} seconds",
        },
    )


@router.get("/ram/duration/{duration}", status_code=status.HTTP_200_OK)
async def full_cpu(duration: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(create_full_rem_process, duration)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "full_type": "mem",
            "duration": duration,
            "message": f"full memory in {duration} seconds",
        },
    )


@router.get("/enque/{num}", status_code=status.HTTP_200_OK)
async def enque(num: int):
    enqueue_task(num)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"enque {num}"},
    )
