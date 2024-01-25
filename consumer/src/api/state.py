from fastapi import APIRouter, Depends, HTTPException, status
from typing import List


# archive
router = APIRouter(
    prefix="/state",
    tags=["State"],
    deprecated=True,
)


@router.get("/cpu/{rate}/duration/{duration}", status_code=status.HTTP_200_OK)
async def state_cpu(rate: str, duration: int):
    return {"state": rate, "duration": duration}


@router.get("/ram/{rate}/duration/{duration}", status_code=status.HTTP_200_OK)
async def state_mem(rate: str, duration: int):
    return {"state": rate, "duration": duration}


@router.get("/sleep/{duration}", status_code=status.HTTP_200_OK)
async def state_sleep(duration: int):
    return {"state": "sleep", "duration": duration}
