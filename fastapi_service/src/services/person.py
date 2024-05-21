from functools import lru_cache
from typing import Annotated, List, Optional

from fastapi import Depends

from fastapi_service.src.core.config import settings
from fastapi_service.src.models.film import FilmShort
from fastapi_service.src.models.person import Person
from fastapi_service.src.services.elasticsearch import ElasticsearchService


class PersonService:
    """
    Contains business logic for working with persons.
    """

    def __init__(self, elasticsearch_service: ElasticsearchService):
        """
        Initialize the service with an Elasticsearch service instance.

        :param elasticsearch_service: An instance of ElasticsearchService.
        """
        self.elasticsearch_service = elasticsearch_service

    async def get_person_by_id(self, person_id: str) -> Optional[Person]:
        """
        Retrieve a person by their ID (UUID).
        May return None if the person is not found.

        :param person_id: The ID of the person to retrieve.
        :return: A Person object if found, otherwise None.
        """
        data = await self.elasticsearch_service.get_model_by_id(index=settings.eks.persons_index, model_id=person_id)
        if not data:
            return None

        return Person(**data)

    async def get_films_by_person_id(
        self,
        *,
        person_id: str,
        page_size: int,
        page_number: int,
        sort: Optional[List[str]] = None,
    ) -> List[FilmShort]:
        """
        Retrieve a list of films associated with a person.

        :param person_id: The ID of the person.
        :param page_size: Number of films per page.
        :param page_number: The page number to retrieve.
        :param sort: Sorting criteria for the films.
        :return: A list of FilmPerson objects.
        """
        query_match = {
            "bool": {
                "must": {"term": {"id": person_id}},
                "filter": {
                    "nested": {
                        "path": "films",
                        "query": {"match_all": {}},
                        "inner_hits": {
                            "size": page_size,
                            "from": self.elasticsearch_service.calculate_offset(page_number, page_size),
                        },
                    }
                },
            }
        }

        data = await self.elasticsearch_service.search_models(
            index=settings.eks.persons_index,
            query_match=query_match,
            page_number=page_number,
            page_size=page_size,
            sort=sort,
        )

        if not data:
            return []

        data_films = data[0]["inner_hits"]["films"]["hits"]["hits"]

        if not data_films:
            return []

        return [FilmShort(**row["_source"]) for row in data_films]

    async def fetch_persons(
        self,
        *,
        page_size: int,
        page_number: int,
        sort: Optional[List[str]] = None,
    ) -> List[Person]:
        """
        Retrieve a list of persons based on the given parameters.
        May return an empty list if no persons are found.

        :param page_size: Number of persons per page.
        :param page_number: The page number to retrieve.
        :param sort: Sorting criteria for the persons.
        :return: A list of Person objects.
        """
        data = await self.elasticsearch_service.search_models(
            index=settings.es.persons_index, page_number=page_number, page_size=page_size, sort=sort
        )

        if not data:
            return []

        return [Person(**row["_source"]) for row in data]

    async def search_persons(
        self,
        *,
        page_size: int,
        page_number: int,
        query: str,
        sort: Optional[List[str]] = None,
    ) -> List[Person]:
        """
        Retrieve a list of persons based on a search query.
        May return an empty list if no persons match the query.

        :param page_size: Number of persons per page.
        :param page_number: The page number to retrieve.
        :param query: The search query string.
        :param sort: Sorting criteria for the persons.
        :return: A list of Person objects.
        """
        query_match = (
            {
                "multi_match": {
                    "query": query,
                    "fuzziness": "auto",
                    "fields": ["full_name"],
                }
            }
            if query
            else None
        )

        data = await self.elasticsearch_service.search_models(
            index=settings.eks.persons_index,
            query_match=query_match,
            page_number=page_number,
            page_size=page_size,
            sort=sort,
        )

        if not data:
            return []

        return [Person(**row["_source"]) for row in data]


@lru_cache()
def get_person_service(
    elasticsearch_service: Annotated[ElasticsearchService, Depends()],
) -> PersonService:
    """
    Provider for PersonService.

    :param elasticsearch_service: An instance of ElasticsearchService.
    :return: An instance of PersonService.
    """
    return PersonService(elasticsearch_service)
