from functools import lru_cache
from typing import Annotated, List, Optional

from fastapi import Depends

from fastapi_service.src.core.config import settings
from fastapi_service.src.models.genre import Genre
from fastapi_service.src.services.elasticsearch import ElasticsearchService


class GenreService:
    """
    Contains business logic for working with genres.
    """

    def __init__(self, elasticsearch_service: ElasticsearchService):
        """
        Initialize the service with an Elasticsearch service instance.

        :param elasticsearch_service: An instance of ElasticsearchService.
        """
        self.elasticsearch_service = elasticsearch_service

    async def fetch_genres(
        self,
        *,
        page_size: int,
        page_number: int,
        sort: Optional[List[str]] = None,
    ) -> List[Genre]:
        """
        Retrieve a list of genres based on the given parameters.
        May return an empty list if no genres are found.

        :param page_size: Number of genres per page.
        :param page_number: The page number to retrieve.
        :param sort: Sorting criteria for the genres.
        :return: A list of Genre objects.
        """
        data = await self.elasticsearch_service.search_models(
            index=settings.eks.genres_index, page_number=page_number, page_size=page_size, sort=sort
        )

        if not data:
            return []

        return [Genre(**row["_source"]) for row in data]

    async def search_genres(
        self,
        *,
        page_size: int,
        page_number: int,
        query: str,
        sort: Optional[List[str]] = None,
    ) -> List[Genre]:
        """
        Retrieve a list of genres based on a search query.
        May return an empty list if no genres match the query.

        :param page_size: Number of genres per page.
        :param page_number: The page number to retrieve.
        :param query: The search query string.
        :param sort: Sorting criteria for the genres.
        :return: A list of Genre objects.
        """
        query_match = (
            {
                "multi_match": {
                    "query": query,
                    "fuzziness": "auto",
                    "fields": [
                        "name",
                        "description",
                    ],
                }
            }
            if query
            else None
        )

        data = await self.elasticsearch_service.search_models(
            index=settings.es.genres_index, query=query_match, page_number=page_number, page_size=page_size, sort=sort
        )

        if not data:
            return []

        return [Genre(**row["_source"]) for row in data]

    async def get_genre_by_id(self, genre_id: str) -> Optional[Genre]:
        """
        Retrieve a genre by its ID (UUID).
        Returns None if the genre is not found.

        :param genre_id: The ID of the genre to retrieve.
        :return: A Genre object if found, otherwise None.
        """
        data = await self.elasticsearch_service.get_model_by_id(index=settings.eks.genres_index, model_id=genre_id)
        if not data:
            return None
        return Genre(**data)


@lru_cache()
def get_genre_service(
    elasticsearch_service: Annotated[ElasticsearchService, Depends()],
) -> GenreService:
    """
    Provider for GenreService.

    :param elasticsearch_service: An instance of ElasticsearchService.
    :return: An instance of GenreService.
    """
    return GenreService(elasticsearch_service)
