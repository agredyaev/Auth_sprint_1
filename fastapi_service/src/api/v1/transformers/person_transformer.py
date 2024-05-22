from fastapi_service.src.api.v1.models_response.person import (
    DefaultFilmPersonResponse,
    DefaultPersonFilmResponse,
    DefaultPersonResponse,
    DetailedPersonResponse,
)
from fastapi_service.src.api.v1.transformers.base_transformer import BaseTransformer
from fastapi_service.src.core.logger import setup_logging
from fastapi_service.src.models.film import FilmShort
from fastapi_service.src.models.person import Person

logger = setup_logging(logger_name=__name__)


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
        films = [DefaultPersonFilmResponse(uuid=film.id, title=film.title, roles=film.roles) for film in person.films]
        return DetailedPersonResponse(uuid=person.id, full_name=person.full_name, films=films)


class DefaultPersonFilmTransformer(BaseTransformer):
    """
    Transforms a Person object into a DefaultPersonFilmResponse object
    """

    def to_response(self, film: FilmShort = None) -> DefaultFilmPersonResponse:
        return DefaultFilmPersonResponse(uuid=film.id, title=film.title, imdb_rating=film.imdb_rating)
