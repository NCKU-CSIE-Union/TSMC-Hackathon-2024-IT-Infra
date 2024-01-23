from fastapi import APIRouter, status

router = APIRouter(prefix="", tags=["Health"])


@router.get("/", status_code=status.HTTP_200_OK)
async def health():
    return {"hello": "world"}
