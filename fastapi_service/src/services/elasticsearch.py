from typing import Annotated, Any

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from fastapi_service.src.core.logger import setup_logging
from fastapi_service.src.db.elasticsearch import get_elastic
from fastapi_service.src.services.exceptions import BadRequestError
from fastapi_service.src.services.redis_cache import ModelCacheDecorator, QueryCacheDecorator

logger = setup_logging(logger_name=__name__)


class ElasticsearchService:
    """
    Contains business logic for working with Elasticsearch.
    """

    def __init__(self, elasticsearch_client: Annotated[AsyncElasticsearch, Depends(get_elastic)]):
        """
        Initialize the service with an Elasticsearch client.

        :param elasticsearch_client: The Elasticsearch client.
        """
        self.elasticsearch_client = elasticsearch_client

    @ModelCacheDecorator(key="model_id")
    async def get_model_by_id(self, *, index: str, model_id: str) -> dict[str, Any] | None:
        """
        Retrieve a specific model by ID from the Elasticsearch index.

        :param index: The name of the Elasticsearch index.
        :param model_id: The ID of the model to retrieve.
        :return: The model data if found, otherwise None.
        """
        return await self._fetch_model(index=index, model_id=model_id)

    async def _fetch_model(self, index: str, model_id: str) -> dict[str, Any] | None:
        """
        Retrieve a specific model by ID from the Elasticsearch index.

        :param index: The name of the Elasticsearch index.
        :param model_id: The ID of the model to retrieve.
        :return: The model data if found, otherwise None.
        """
        try:
            document = await self.elasticsearch_client.get(index=index, id=model_id)
        except NotFoundError:
            logger.info(f"Model with ID {model_id} not found in index {index}.")
            return None
        except BadRequestError as e:
            logger.error(f"Failed to fetch model with ID {model_id} from index {index}.")
            raise BadRequestError(status_code=e.status_code, message=e.message, body=e.body, errors=e.errors) from e

        return document["_source"]

    @staticmethod
    def calculate_offset(page_number: int | None, page_size: int | None) -> int | None:
        """
        Calculate the offset for pagination.

        :param page_number: The page number for pagination.
        :param page_size: The number of items per page.
        :return: The offset value for pagination.
        """
        if page_number is not None and page_size is not None:
            return (page_number - 1) * page_size
        return None

    @staticmethod
    def format_sort_criteria(sort: list[str] | None) -> list[str] | None:
        """
        Parse and format the sort criteria for Elasticsearch.

        :param sort: The sorting criteria.
        :return: The formatted sorting criteria.
        """
        if sort is not None:
            return [f"{item[1:]}:desc" if item.startswith("-") else item for item in sort]
        return sort

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
        """
        Search for models in the Elasticsearch index with pagination and optional sorting.

        :param index: The name of the Elasticsearch index.
        :param page_number: The page number for pagination.
        :param page_size: The number of items per page.
        :param query_match: The query match conditions.
        :param sort: The sorting criteria.
        :return: The list of matching models, or None if no matches are found.
        """
        return await self._perform_search(
            index=index, query=query_match, page_number=page_number, page_size=page_size, sort=sort
        )

    async def _perform_search(
        self,
        index: str,
        query: dict[str, Any] | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        sort: list[str] | None = None,
    ) -> list[dict[str, Any]] | None:
        """
        Perform a search query on the Elasticsearch index.

        :param index: The name of the Elasticsearch index.
        :param query: The query match conditions.
        :param page_number: The page number for pagination.
        :param page_size: The number of items per page.
        :param sort: The sorting criteria.
        :return: The list of matching models, or None if no matches are found.
        """
        try:
            documents = await self.elasticsearch_client.search(
                index=index,
                query=query,
                sort=self.format_sort_criteria(sort),
                size=page_size,
                from_=self.calculate_offset(page_number, page_size),
            )
        except NotFoundError:
            logger.info(f"No documents found in index {index}.")
            return None
        except BadRequestError as exp:
            logger.error(f"Failed to search in index {index}.")
            raise BadRequestError(
                status_code=exp.status_code, message=exp.message, body=exp.body, errors=exp.errors
            ) from exp

        return documents["hits"]["hits"]
