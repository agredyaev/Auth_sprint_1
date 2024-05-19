from fastapi.routing import APIRouter

from fastapi_service.src.api.v1.films import router as films_router
from fastapi_service.src.api.v1.genres import router as genres_router
from fastapi_service.src.api.v1.persons import router as persons_router

router = APIRouter()
router.include_router(films_router)
router.include_router(genres_router)
router.include_router(persons_router)
