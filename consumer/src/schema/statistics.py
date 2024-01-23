from pydantic import BaseModel


class HardwareResponse(BaseModel):
    percent: float
    usage: float
