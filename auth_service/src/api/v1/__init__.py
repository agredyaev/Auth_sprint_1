from fastapi.routing import APIRouter

from auth_service.src.api.v1.auth import auth_router
from auth_service.src.api.v1.role import role_router


router = APIRouter()
router.include_router(auth_router)
router.include_router(role_router)
