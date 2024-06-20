from typing import AsyncGenerator

import pytest_asyncio
from redis.asyncio import Redis


@pytest_asyncio.fixture(scope="session")
async def cache_client() -> AsyncGenerator[Redis, None]:
    from tests.auth_service.settings import config

    async with Redis(
        host=config.infra.redis.host,
        port=config.infra.redis.port,
        username=config.infra.redis.dsn.username,
        password=config.infra.redis.dsn.password,
        db=config.infra.redis.db_number,
    ) as client:
        yield client


@pytest_asyncio.fixture
async def get_all_keys(cache_client):
    async def _get_all_keys(pattern="auth:*"):
        keys = await cache_client.keys(pattern)

        return keys

    return _get_all_keys


@pytest_asyncio.fixture
async def flush_tokens(cache_client):
    async def _flush():
        await cache_client.flushall()

    return _flush


@pytest_asyncio.fixture
async def add_to_deny_list(cache_client, get_all_keys):
    async def _add_to_deny_list():
        new_token = await get_all_keys()
        if not new_token:
            raise ValueError("No tokens to add to deny list")
        for token in new_token:
            before = await cache_client.get(token)
            await cache_client.set(name=token, value="true")
            after = await cache_client.get(token)
        return before, after

    return _add_to_deny_list
