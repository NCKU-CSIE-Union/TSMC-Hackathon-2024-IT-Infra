from fastapi import APIRouter, Depends, HTTPException, status
from typing import List


router = APIRouter(
    prefix="/full",
    tags=["Full"],
)


@router.get("/cpu/duration/{duration}", status_code=status.HTTP_200_OK)
async def full_cpu(cpu_rate: int, duration: int):
    return {"cpu_rate": cpu_rate, "duration": duration}


@router.get("/mem/duration/{duration}", status_code=status.HTTP_200_OK)
async def full_cpu(mem_rate: int, duration: int):
    return {"mem_rate": mem_rate, "duration": duration}


@router.get("/enque/{num}", status_code=status.HTTP_200_OK)
async def enque(num: int):
    return {"num": num}
