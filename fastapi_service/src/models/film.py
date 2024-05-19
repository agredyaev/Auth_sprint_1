from pydantic import Field

from fastapi_service.src.models.mixins import IdMixin, NameMixin, ORJSONMixin


class FilmPerson(IdMixin, NameMixin):
    """Defines film person model"""


class FilmGenre(IdMixin, NameMixin):
    """Defines film genre model"""


class Film(ORJSONMixin, IdMixin):
    """Defines film model"""

    imdb_rating: float | None = Field(None)
    title: str
    description: str | None = Field("")

    genres: list[FilmGenre]
    genres_names: list[str]

    directors: list[FilmPerson]
    directors_names: list[str]

    actors: list[FilmPerson]
    actors_names: list[str]

    writers: list[FilmPerson]
    writers_names: list[str]
