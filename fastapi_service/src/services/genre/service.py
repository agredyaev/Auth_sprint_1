from typing import Optional

from fastapi_service.src.core.config import settings
from fastapi_service.src.models.genre import Genre
from fastapi_service.src.services.elasticsearch.model_service import ModelService
from fastapi_service.src.services.elasticsearch.search_service import SearchService


class GenreService:
    """
    Contains business logic for working with genres.
    """

    def __init__(self, model_service: ModelService, search_service: SearchService):
        self.model_service = model_service
        self.search_service = search_service

    async def fetch_genres(
        self,
        *,
        page_size: int,
        page_number: int,
        sort: Optional[list[str]] = None,
    ) -> list[Genre]:
        """
        Retrieve a list of genres based on the given parameters.
        May return an empty list if no genres are found.

        :param page_size: Number of genres per page.
        :param page_number: The page number to retrieve.
        :param sort: Sorting criteria for the genres.
        :return: A list of Genre objects.
        """
        data = await self.search_service.search_models(
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
        sort: Optional[list[str]] = None,
    ) -> list[Genre]:
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

        data = await self.search_service.search_models(
            index=settings.es.genres_index, query=query_match, page_number=page_number, page_size=page_size, sort=sort
        )

        if not data:
            return []

        return [Genre(**row["_source"]) for row in data]

    async def get_genre_by_id(self, genre_id: str) -> Optional[Genre]:
        """
        Retrieve a genre by its ID (UUID).
        Returns None if the genre is not found.
        """
        data = await self.model_service.get_model_by_id(index=settings.eks.genres_index, model_id=genre_id)
        if not data:
            return None
        return Genre(**data)
