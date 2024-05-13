from elasticsearch import AsyncElasticsearch
from fastapi_service.src.core.config import settings
from fastapi_service.src.core.exceptions import ElasticsearchConnectionError
from fastapi_service.src.core.logger import setup_logging

logger = setup_logging()

es: AsyncElasticsearch | None = None


async def es_open():
    global es
    es = AsyncElasticsearch(
        hosts=[settings.eks.dsn],
    )


async def get_elastic() -> AsyncElasticsearch:
    """
    Get Elasticsearch instance
    :return Elasticsearch instance
    """
    if es is None:
        logger.critical("ES is not initialized")
        raise ElasticsearchConnectionError("Elasticsearch client has not been initialized.")
    return es
