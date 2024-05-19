from fastapi_service.src.api.v1.transformers.base_transformer import BaseTransformer
from fastapi_service.src.models.person import Person
from fastapi_service.src.api.v1.models_response.person import DefaultPersonResponse, DetailedPersonResponse, \
    DefaultFilmPersonResponse


class DefaultPersonTransformer(BaseTransformer):
    """
    Transforms a Person object into a DefaultPersonResponse object
    """

    def to_response(self, person: Person = None) -> DefaultPersonResponse:
        return DefaultPersonResponse(uuid=person.id, full_name=person.full_name)


class DetailedPersonTransformer(BaseTransformer):
    """
    Transforms a Person object into a DetailedPersonResponse object
    """

    def to_response(self, person: Person = None) -> DetailedPersonResponse:
        return DetailedPersonResponse(uuid=person.id, full_name=person.full_name)


class DefaultFilmPersonTransformer(BaseTransformer):
    """
    Transforms a Person object into a DefaultFilmPersonResponse object
    """

    def to_response(self, person: Person = None) -> DefaultFilmPersonResponse:
        return DefaultFilmPersonResponse(uuid=person.id, title=person.title, roles=person.roles)
