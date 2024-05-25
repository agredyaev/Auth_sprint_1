import pytest_asyncio
from redis.asyncio import Redis

from tests.functional.settings import config


@pytest_asyncio.fixture(scope="session")
async def cache_client():
    async with Redis(host=config.infra.redis.host, port=config.infra.redis.port) as client:
        yield client


@pytest_asyncio.fixture(scope="session", name="clear_cache")
async def clear_cache(cache_client):
    await cache_client.flushall()
