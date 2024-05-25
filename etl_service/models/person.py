from pydantic import Field

from etl_service.models.mixins import IdMixin


class PersonFilmwork(IdMixin):
    """Defines person filmwork model"""

    title: str
    roles: list[str]
    rating: float | None = Field(default=None, serialization_alias="imdb_rating")


class Person(IdMixin):
    full_name: str = Field(...)
    movies: list[PersonFilmwork] = Field(default_factory=list, serialization_alias="films")
