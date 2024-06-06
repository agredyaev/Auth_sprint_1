import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from tests.fastapi_service.settings import config


@pytest_asyncio.fixture(scope="session", name="es_client")
async def es_client():
    async with AsyncElasticsearch(hosts=[config.infra.es.dsn]) as client:
        yield client


@pytest_asyncio.fixture(scope="session", name="clear_es_data")
async def clear_es_data(es_client: AsyncElasticsearch):
    await es_client.indices.delete(index="_all")
