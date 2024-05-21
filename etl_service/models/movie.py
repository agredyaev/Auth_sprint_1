from typing import Optional, Union

from pydantic import Field

from etl_service.models.mixins import IdMixin, NameMixin
from etl_service.utility.logger import setup_logging

logger = setup_logging()


class Person(IdMixin, NameMixin):
    """Defines person model"""


class Genre(IdMixin, NameMixin):
    """Defines genre model"""


class Filmwork(IdMixin):
    """Defines filmwork model"""

    rating: Union[str, float, None] = Field(default=None, serialization_alias="imdb_rating")
    title: str
    description: Optional[str] = None
    genres_names: Optional[list[str]] = Field(default_factory=list, serialization_alias="genres_names")
    genres: list[Genre] = Field(default_factory=list, serialization_alias="genres")
    directors_names: Optional[list[str]] = Field(default_factory=list, serialization_alias="directors_names")
    directors: list[Person] = Field(default_factory=list, serialization_alias="directors")
    actors_names: Optional[list[str]] = Field(default_factory=list, serialization_alias="actors_names")
    actors: list[Person] = Field(default_factory=list, serialization_alias="actors")
    writers_names: Optional[list[str]] = Field(default_factory=list, serialization_alias="writers_names")
    writers: list[Person] = Field(default_factory=list, serialization_alias="writers")
