from typing import List

from fastapi_service.src.api.v1.transformers.base_transformer import BaseTransformer
from fastapi_service.src.models.film import Film, FilmPerson, FilmGenre
from fastapi_service.src.api.v1.models_response.film import DetailedFilmResponse, DefaultFilmResponse
from fastapi_service.src.api.v1.models_response.person import DefaultPersonResponse
from fastapi_service.src.api.v1.models_response.genre import DefaultGenreResponse


class DefaultFilmTransformer(BaseTransformer):
    """
    Transform a Film object into a DefaultFilmResponse object.
    """
    def to_response(self, film: Film = None) -> DefaultFilmResponse:
        return DefaultFilmResponse(
            uuid=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
        )


class DetailedFilmTransformer(BaseTransformer):
    """
    Transform a Film object into a DetailedFilmResponse object.
    """

    def to_response(self, film: Film = None) -> DetailedFilmResponse:
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
    def _transform_person(person: FilmPerson) -> DefaultPersonResponse:
        return DefaultPersonResponse(uuid=person.id, full_name=person.full_name)

