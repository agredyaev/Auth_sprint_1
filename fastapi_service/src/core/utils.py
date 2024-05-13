from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi_service.src.db import elasticsearch, redis


@asynccontextmanager
async def lifespan(_: FastAPI):
    await redis.redis_open()
    await elasticsearch.es_open()
    yield
    await redis.redis.close()
    await elasticsearch.es.close()
