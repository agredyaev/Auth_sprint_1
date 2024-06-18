from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter


@asynccontextmanager
async def get_lifespan(_: FastAPI) -> AsyncIterator[None]:
    from auth_service.src.db import redis

    """
    Lifespan function for FastAPI
    """
    try:
        await redis.redis_open()
        await FastAPILimiter.init(redis=redis.redis)
        yield
    finally:
        if redis.redis is not None:
            await redis.redis.close()
