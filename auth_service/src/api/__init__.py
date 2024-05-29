from fastapi.routing import APIRouter

from auth_service.src.api.v1 import router as v1_router
from auth_service.src.api.healthcheck import healthcheck_router

router = APIRouter()
router.include_router(v1_router, prefix="/v1")
router.include_router(healthcheck_router)