from typing import Any

from elasticsearch import NotFoundError

from fastapi_service.src.core.exceptions import BadRequestError
from fastapi_service.src.core.config import settings
from fastapi_service.src.core.logger import setup_logging
from fastapi_service.src.services.elasticsearch.client import ElasticsearchClientProtocol
from fastapi_service.src.services.redis.cache import QueryCacheDecorator

logger = setup_logging(logger_name=__name__)


class SearchService:
    def __init__(self, client: ElasticsearchClientProtocol):
        self.client = client

    @QueryCacheDecorator()
    async def search_models(
        self,
        *,
        index: str,
        page_number: int,
        page_size: int,
        query_match: dict[str, Any] | None = None,
        sort: list[str] | None = None,
    ) -> list[dict[str, Any]] | None:
        return await self._perform_search(
            index=index, query=query_match, page_number=page_number, page_size=page_size, sort=sort
        )

    async def _perform_search(
        self,
        index: str,
        query: dict[str, Any] = settings.eks.query,
        page_number: int = settings.eks.page_number,
        page_size: int = settings.eks.page_size,
        sort: list[str] = settings.eks.sort,
    ) -> list[dict[str, Any]] | None:
        try:
            documents = await self.client.search(
                index=index,
                query=query,
                sort=self.format_sort_criteria(sort),
                size=page_size,
                from_=self.calculate_offset(page_number, page_size),
            )
            return documents

        except NotFoundError as e:
            logger.info(f"No documents found in index {index} {e}")
            return None

        except BadRequestError as e:
            logger.error(f"Failed to search in index {index} {e}")
            return None

        except Exception as e:
            logger.exception(f"Failed to search in index {index}: {e}")
            return None

    @staticmethod
    def calculate_offset(page_number: int | None, page_size: int | None) -> int | None:
        if page_number is not None and page_size is not None:
            return (page_number - 1) * page_size
        return None

    @staticmethod
    def format_sort_criteria(sort: list[str] | None) -> list[str] | None:
        if sort is not None:
            return [f"{item[1:]}:desc" if item.startswith("-") else item for item in sort]
        return sort
