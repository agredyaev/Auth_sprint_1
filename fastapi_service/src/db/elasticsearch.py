from elasticsearch import AsyncElasticsearch

from fastapi_service.src.core.config import settings
from fastapi_service.src.core.exceptions import ElasticsearchConnectionError
from fastapi_service.src.core.logger import setup_logging

logger = setup_logging(logger_name=__name__)

es: AsyncElasticsearch | None = None


async def es_open() -> None:
    """
    Open Elasticsearch connection
    """
    global es
    if es is None:
        es = AsyncElasticsearch(
            hosts=[settings.eks.dsn.unicode_string()],
        )
        logger.info("Elasticsearch client has been initialized.")


async def es_close() -> None:
    """
    Close Elasticsearch connection
    """
    global es
    if es is not None:
        await es.close()
        logger.info("Elasticsearch client has been closed.")


async def get_elastic() -> AsyncElasticsearch:
    """
    Get Elasticsearch instance
    :return Elasticsearch instance
    """
    if es is None:
        logger.critical("ES is not initialized")
        raise ElasticsearchConnectionError("Elasticsearch client has not been initialized.")
    return es
