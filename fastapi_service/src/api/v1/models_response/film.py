from fastapi_service.src.api.v1.models_response.genre import DefaultGenreResponse
from fastapi_service.src.api.v1.models_response.mixins import NameMixin, TitleMixin, UUIDMixin


class DefaultFilmResponse(UUIDMixin, TitleMixin):
    imdb_rating: float | None


class DefaultFilmPersonResponse(UUIDMixin, NameMixin):
    pass


class DetailedFilmResponse(DefaultFilmResponse):
    description: str | None
    genres: list[DefaultGenreResponse]
    actors: list[DefaultFilmPersonResponse]
    writers: list[DefaultFilmPersonResponse]
    directors: list[DefaultFilmPersonResponse]
