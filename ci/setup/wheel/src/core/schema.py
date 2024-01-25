from pydantic import BaseModel


class AuthRequest(BaseModel):
    token: str
