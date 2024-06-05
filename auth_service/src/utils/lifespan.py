from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from auth_service.src.db import postgres, redis

@asynccontextmanager
async def get_lifespan(_: FastAPI) -> AsyncIterator[None]:
    """
    Lifespan function for FastAPI
    """
    await redis.redis_open()
    yield
    if redis.redis:
        await redis.redis.close()