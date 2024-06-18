from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from starlette import status

router = APIRouter()


@router.get("/healthcheck")
async def health_check() -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "ok"},
    )
