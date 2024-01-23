from pydantic import BaseModel


class HardwareResponse(BaseModel):
    percent: float
    usage: float


class StatisticsResponse(BaseModel):
    cpu: HardwareResponse
    mem: HardwareResponse
    remain_count: int
    avg_exe_time: float