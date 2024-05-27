from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/healthcheck")
async def health_check():
    return JSONResponse(
        status_code=200,
        content={"status": "ok"},
    )
