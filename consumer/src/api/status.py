from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

# services
from services.statistics import (
    get_cpu_percent,
    get_cpu_usage,
    get_mem_percent,
    get_mem_usage,
    get_remain_count,
    get_avg_exe_time,
)

# schemas
from schema.statistics import HardwareResponse


router = APIRouter(prefix="/status", tags=["Status"])


@router.get("/cpu", status_code=status.HTTP_200_OK, response_model=HardwareResponse)
async def status_cpu():
    """
    - percent: cpu usage percentage
    - usage: cpu usage percentage
    """
    return HardwareResponse(percent=get_cpu_percent(), usage=get_cpu_usage())


@router.get("/mem", status_code=status.HTTP_200_OK, response_model=HardwareResponse)
async def status_mem():
    """
    - percent: memory usage percentage
    - usage: memory usage in **GB**
    """
    return HardwareResponse(percent=get_mem_percent(), usage=get_mem_usage())


@router.get("/remain_count", status_code=status.HTTP_200_OK, response_model=int)
async def remain_count():
    return get_remain_count()


@router.get("/avg_exe_time", status_code=status.HTTP_200_OK, response_model=float)
async def avg_exe_time():
    return get_avg_exe_time()


@router.get("/log", status_code=status.HTTP_200_OK)
async def log():
    return {"log": "log"}
