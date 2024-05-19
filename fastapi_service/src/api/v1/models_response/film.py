from fastapi_service.src.api.v1.models_response.person import DefaultPersonResponse
from fastapi_service.src.api.v1.models_response.genre import DefaultGenreResponse
from fastapi_service.src.api.v1.models_response.mixins import UUIDMixin, TitleMixin


class DefaultFilmResponse(UUIDMixin, TitleMixin):
    imdb_rating: float | None
    genres: list[str]


class DetailedFilmResponse(DefaultFilmResponse):
    description: str | None
    genres: list[DefaultGenreResponse]
    actors: list[DefaultPersonResponse]
    writers: list[DefaultPersonResponse]
    directors: list[DefaultPersonResponse]
