from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from auth_service.src.db import redis


@asynccontextmanager
async def get_lifespan(_: FastAPI) -> AsyncIterator[None]:
    """
    Lifespan function for FastAPI
    """
    try:
        await redis.redis_open()
        yield
    finally:
        await redis.redis.close()
