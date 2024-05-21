from fastapi_service.src.api.v1.models_response.mixins import TitleMixin, UUIDMixin


class DefaultFilmPersonResponse(UUIDMixin, TitleMixin):
    imdb_rating: float | None


class DefaultPersonFilmResponse(UUIDMixin, TitleMixin):
    roles: list[str]


class DefaultPersonResponse(UUIDMixin):
    full_name: str


class DetailedPersonResponse(DefaultPersonResponse):
    films: list[DefaultPersonFilmResponse]
