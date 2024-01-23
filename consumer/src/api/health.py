from fastapi import APIRouter, Depends, HTTPException, status
from typing import List


router = APIRouter(prefix="", tags=["Health"]   )


@router.get("/", status_code=status.HTTP_200_OK)
async def health():
    return {"hello": "world"}
