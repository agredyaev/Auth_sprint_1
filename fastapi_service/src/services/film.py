from functools import lru_cache
from typing import Annotated, Any, Dict, List, Optional

from fastapi import Depends

from fastapi_service.src.core.config import settings
from fastapi_service.src.models.film import Film
from fastapi_service.src.services.elasticsearch import ElasticsearchService


class FilmService:
    """
    Contains business logic for working with films.
    """

    def __init__(self, elasticsearch_service: ElasticsearchService):
        """
        Initialize the service with an Elasticsearch service instance.

        :param elasticsearch_service: An instance of ElasticsearchService.
        """
        self.elasticsearch_service = elasticsearch_service

    async def get_films(
        self, *, page_size: int, page_number: int, sort: Optional[List[str]] = None, genre: Optional[List[str]] = None
    ) -> List[Film]:
        """
        Retrieve a list of films based on the given parameters.
        May return an empty list if no films are found.

        :param page_size: Number of films per page.
        :param page_number: The page number to retrieve.
        :param sort: Sorting criteria for the films.
        :param genre: List of genres to filter the films.
        :return: A list of Film objects.
        """
        query_match = None

        if genre:
            query_match = {"terms": {"genres_names": genre, "boost": 1.0}}

        return await self._search_films(
            page_size=page_size, page_number=page_number, sort=sort, query_match=query_match
        )

    async def search_films(
        self,
        *,
        page_size: int,
        page_number: int,
        query: str,
        sort: Optional[List[str]] = None,
    ) -> List[Film]:
        """
        Retrieve a list of films based on a search query.
        May return an empty list if no films match the query.

        :param page_size: Number of films per page.
        :param page_number: The page number to retrieve.
        :param query: The search query string.
        :param sort: Sorting criteria for the films.
        :return: A list of Film objects.
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
        self, *, page_size: int, page_number: int, sort: Optional[List[str]], query_match: Optional[Dict[str, Any]]
    ) -> List[Film]:
        """
        Helper method to perform search queries on the Elasticsearch index.

        :param page_size: Number of films per page.
        :param page_number: The page number to retrieve.
        :param sort: Sorting criteria for the films.
        :param query_match: The query match conditions.
        :return: A list of Film objects.
        """
        data = await self.elasticsearch_service.search_models(
            index=settings.es.films_index,
            page_number=page_number,
            page_size=page_size,
            query_match=query_match,
            sort=sort,
        )

        if not data:
            return []

        return [Film(**row["_source"]) for row in data]

    async def get_film_by_id(self, film_id: str) -> Optional[Film]:
        """
        Retrieve a film by its ID (UUID).
        May return None if the film is not found.

        :param film_id: The ID of the film to retrieve.
        :return: A Film object if found, otherwise None.
        """
        data = await self.elasticsearch_service.get_model_by_id(index=settings.es.films_index, model_id=film_id)
        if not data:
            return None

        return Film(**data)


@lru_cache()
def get_film_service(
    elasticsearch_service: Annotated[ElasticsearchService, Depends()],
) -> FilmService:
    """
    Provider for FilmService.

    :param elasticsearch_service: An instance of ElasticsearchService.
    :return: An instance of FilmService.
    """
    return FilmService(elasticsearch_service)
