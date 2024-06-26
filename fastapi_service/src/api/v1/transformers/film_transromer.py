from fastapi_service.src.api.v1.models_response.film import (
    DefaultFilmPersonResponse,
    DefaultFilmResponse,
    DetailedFilmResponse,
)
from fastapi_service.src.api.v1.models_response.genre import DefaultGenreResponse
from fastapi_service.src.api.v1.transformers.base_transformer import BaseTransformer
from fastapi_service.src.models.film import Film, FilmGenre, FilmPerson


class DefaultFilmTransformer(BaseTransformer):
    """
    Transform a Film object into a DefaultFilmResponse object.
    """

    def to_response(self, film: Film) -> DefaultFilmResponse:
        return DefaultFilmResponse(
            uuid=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
        )


class DetailedFilmTransformer(BaseTransformer):
    """
    Transform a Film object into a DetailedFilmResponse object.
    """

    def to_response(self, film: Film) -> DetailedFilmResponse:
        return DetailedFilmResponse(
            uuid=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
            description=film.description if film.description is not None else "",
            genres=[self._transform_genre(genre) for genre in film.genres],
            actors=[self._transform_person(person) for person in film.actors],
            writers=[self._transform_person(person) for person in film.writers],
            directors=[self._transform_person(person) for person in film.directors],
        )

    @staticmethod
    def _transform_genre(genre: FilmGenre) -> DefaultGenreResponse:
        return DefaultGenreResponse(uuid=genre.id, name=genre.name)

    @staticmethod
    def _transform_person(person: FilmPerson) -> DefaultFilmPersonResponse:
        return DefaultFilmPersonResponse(uuid=person.id, name=person.name)
