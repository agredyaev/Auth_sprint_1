from fastapi_service.src.core.config import settings
from fastapi_service.src.models.film import FilmShort
from fastapi_service.src.models.person import Person
from fastapi_service.src.services.elasticsearch.model_service import ModelService
from fastapi_service.src.services.elasticsearch.search_service import SearchService


class PersonService:
    """
    Contains business logic for working with persons.
    """

    def __init__(self, model_service: ModelService, search_service: SearchService):
        self.model_service = model_service
        self.search_service = search_service

    async def get_person_by_id(self, person_id: str) -> Person | None:
        """
        Retrieve a person by their ID (UUID).
        May return None if the person is not found.
        """
        data = await self.model_service.get_model_by_id(index=settings.eks.persons_index, model_id=person_id)
        if not data:
            return None

        return Person(**data)

    async def get_films_by_person_id(
        self,
        *,
        person_id: str,
        page_size: int,
        page_number: int,
        sort: list[str] | None = None,
    ) -> list[FilmShort]:
        """
        Retrieve a list of films associated with a person.
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
                            "from": self.search_service.calculate_offset(page_number, page_size),
                        },
                    }
                },
            }
        }

        data = await self.search_service.search_models(
            index=settings.eks.persons_index,
            query_match=query_match,
            page_number=page_number,
            page_size=page_size,
            sort=sort,
        )

        if not data:
            return []

        data_films = data[0].get("films")

        if not data_films:
            return []

        return [FilmShort(**row) for row in data_films]

    async def fetch_persons(
        self,
        *,
        page_size: int,
        page_number: int,
        sort: list[str] | None = None,
    ) -> list[Person]:
        """
        Retrieve a list of persons based on the given parameters.
        May return an empty list if no persons are found.
        """
        data = await self.search_service.search_models(
            index=settings.eks.persons_index, page_number=page_number, page_size=page_size, sort=sort
        )

        if not data:
            return []

        return [Person(**row) for row in data]

    async def search_persons(
        self,
        *,
        page_size: int,
        page_number: int,
        query: str,
        sort: list[str] | None = None,
    ) -> list[Person]:
        """
        Retrieve a list of persons based on a search query.
        May return an empty list if no persons match the query.
        """
        query_match = (
            {
                "multi_match": {
                    "query": query,
                    "fuzziness": "AUTO",
                    "fields": ["full_name^3"],
                    "operator": "and",
                }
            }
            if query
            else None
        )

        data = await self.search_service.search_models(
            index=settings.eks.persons_index,
            query_match=query_match,
            page_number=page_number,
            page_size=page_size,
            sort=sort,
        )

        if not data:
            return []

        return [Person(**row) for row in data]
