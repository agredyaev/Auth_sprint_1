from typing import Any

from fastapi_service.src.core.config import settings
from fastapi_service.src.models.film import Film
from fastapi_service.src.services.elasticsearch.model_service import ModelService
from fastapi_service.src.services.elasticsearch.search_service import SearchService


class FilmService:
    """
    Contains business logic for working with films.
    """

    def __init__(self, model_service: ModelService, search_service: SearchService):
        self.model_service = model_service
        self.search_service = search_service

    async def get_films(
        self, *, page_size: int, page_number: int, sort: list[str] | None = None, genre: str | None = None
    ) -> list[Film]:
        """
        Retrieve a list of films based on the given parameters.
        May return an empty list if no films are found.
        """
        query_match = None

        if genre:
            query_match = {"terms": {"genres_names": genre}}

        return await self._search_films(
            page_size=page_size, page_number=page_number, sort=sort, query_match=query_match
        )

    async def search_films(
        self,
        *,
        page_size: int,
        page_number: int,
        query: str,
        sort: list[str] | None = None,
    ) -> list[Film]:
        """
        Retrieve a list of films based on a search query.
        May return an empty list if no films match the query.
        """
        query_match = None

        if query:
            query_match = {
                "multi_match": {
                    "query": query,
                    "fuzziness": "auto",
                    "fields": [
                        "actors_names",
                        "writers_names",
                        "title",
                        "description",
                        "genres_names",
                        "directors_names",
                    ],
                }
            }

        return await self._search_films(
            page_size=page_size, page_number=page_number, sort=sort, query_match=query_match
        )

    async def _search_films(
        self, *, page_size: int, page_number: int, sort: list[str] | None, query_match: dict[str, Any] | None
    ) -> list[Film]:
        """
        Helper method to perform search queries on the Elasticsearch index.
        """

        data = await self.search_service.search_models(
            index=settings.eks.films_index,
            page_number=page_number,
            page_size=page_size,
            query_match=query_match,
            sort=sort,
        )

        if not data:
            return []

        return [Film(**row) for row in data]

    async def get_film_by_id(self, film_id: str) -> Film | None:
        """
        Retrieve a film by its ID (UUID).
        May return None if the film is not found.
        """
        data = await self.model_service.get_model_by_id(index=settings.eks.films_index, model_id=film_id)
        if not data:
            return None

        return Film(**data)
