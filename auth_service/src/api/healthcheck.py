from fastapi import APIRouter
from fastapi.responses import JSONResponse

healthcheck_router = APIRouter()


@healthcheck_router.get("/healthcheck")
async def health_check():
    return JSONResponse(
        status_code=200,
        content={"status": "ok"},
    )
