from fastapi.routing import APIRouter

from auth_service.src.api.v1.healthcheck import router as healthcheck_router
from auth_service.src.api.v1.roles import router as roles_router
from auth_service.src.api.v1.users import router as users_router

router = APIRouter()
router.include_router(users_router)
router.include_router(roles_router)
router.include_router(healthcheck_router)
