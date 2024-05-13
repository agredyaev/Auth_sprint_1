from fastapi_service.src.models.mixins import NameMixin, IdMixin, ORJSONMixin
from pydantic import Field


class Person(IdMixin, NameMixin):
    """Defines person model"""


class Genre(IdMixin, NameMixin):
    """Defines genre model"""


class Film(ORJSONMixin, IdMixin):
    """Defines film model"""

    imdb_rating: float | None = Field(None)
    title: str
    description: str | None = Field("")

    genres: list[Genre]
    genres_names: list[str]

    directors: list[Person]
    directors_names: list[str]

    actors: list[Person]
    actors_names: list[str]

    writers: list[Person]
    writers_names: list[str]
