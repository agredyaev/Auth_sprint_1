from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from auth_service.src.db import postgres, redis
from auth_service.src.models.entity import Users

@asynccontextmanager
async def get_lifespan(_: FastAPI) -> AsyncIterator[None]:
    """
    Lifespan function for FastAPI
    """
    await postgres.create_database()
    await redis.redis_open()
    yield
    await redis.redis.close()
    await postgres.purge_database()