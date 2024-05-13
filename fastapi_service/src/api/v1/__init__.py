from fastapi.routing import APIRouter

from .films import router as films_router
from .genres import router as genres_router
from .persons import router as persons_router

router = APIRouter()
router.include_router(films_router)
router.include_router(genres_router)
router.include_router(persons_router)
