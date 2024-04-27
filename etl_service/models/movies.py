from typing import Iterable, Optional, Union
from pydantic import Field

from etl_service.models.mixins import IdMixin
from etl_service.utility.logger import setup_logging

logger = setup_logging()


class Genre(IdMixin):
    """Defines genre model"""

    name: str


class Person(IdMixin):
    """Defines person model"""

    name: str


class Filmwork(IdMixin):
    """Defines filmwork model"""

    rating: Union[str, float, None] = None
    title: str
    description: Optional[str] = None
    genres_names: Optional[list[str]] = None
    genres: list[Genre] = Field(default_factory=list)
    directors_names: Optional[list[str]] = None
    directors: list[Person] = Field(default_factory=list)
    actors_names: Optional[list[str]] = None
    actors: list[Person] = Field(default_factory=list)
    writers_names: Optional[list[str]] = None
    writers: list[Person] = Field(default_factory=list)

    @staticmethod
    def _extract_names(objects: Iterable[Union[Person, Genre]]) -> list[str]:
        """Get names from objects"""
        if objects is None:
            return []
        return [obj.name for obj in objects if obj is not None]

    def transform(self) -> None:
        """Transform data into correct format"""

        try:
            self.genres_names = self._extract_names(self.genres)
            self.directors_names = self._extract_names(self.directors)
            self.actors_names = self._extract_names(self.actors)
            self.writers_names = self._extract_names(self.writers)
            self.rating = float(self.rating) if self.rating else None

        except ValueError as e:
            logger.exception("Can't transform data: %s", e)
