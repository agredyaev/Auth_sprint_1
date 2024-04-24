from typing import Optional, Iterable, List, Union
from mixins import IdMixin


class Genre(IdMixin):
    """Defines genre model"""
    name: str


class Person(IdMixin):
    """Defines person model"""
    name: str


class Filmwork(IdMixin):
    """Defines filmwork model"""
    rating: Union[str, Optional[float]]
    title: str
    description: Optional[str]
    type: str
    genres_names: Optional[List[str]]
    genres: List[Genre]
    directors_names: Optional[List[str]]
    directors: List[Person]
    actors_names: Optional[List[str]]
    actors: List[Person]
    writers_names: Optional[List[str]]
    writers: List[Person]

    @staticmethod
    def _extract_names(objects: Iterable[Union[Person, Genre]]):
        """Get names from objects"""
        return [x.name for x in objects]

    def transform(self) -> None:
        """Transform data into correct format"""
        self.genres_names = self._extract_names(self.genres)
        self.directors_names = self._extract_names(self.directors)
        self.actors_names = self._extract_names(self.actors)
        self.writers_names = self._extract_names(self.writers)
        self.rating = float(self.rating) if self.rating else None
