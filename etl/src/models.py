"""
Defines dataclasses for database schema representation. Inherits from BaseModel for
regular entities. For maintaining load order, especially for many-to-many
relationships, inherit from Link class to ensure correct data integration
and relationship handling.
"""

import datetime
import uuid
from dataclasses import dataclass, field, fields
from datetime import date
from typing import ClassVar, List


class BaseModel:
    """
    Provides a mechanism to define the class attributes.
    """
    schema: ClassVar[str]
    table_name: ClassVar[str]
    constraints: ClassVar[List[str]]
    retrieved_fields: ClassVar[List[str]]

    @classmethod
    def get_own_fields(cls):
        """
        Returns a list of field names defined directly in the subclass,
        excluding any fields inherited from base classes.
        """
        own_fields = [f.name for f in fields(
            cls) if f.name in cls.__annotations__]
        return own_fields

    @classmethod
    def check_fields_overridden(cls):
        """
        Checks if all fields of the BaseModel are overridden in the subclass.
        Raises AttributeError if any field is not properly overridden.
        """
        base_fields = set(BaseModel.__annotations__.keys())
        subclass_fields = set(cls.__annotations__.keys())

        not_overridden_fields = base_fields - subclass_fields

        if not_overridden_fields:
            raise AttributeError(f"Subclass {cls.__name__} must override fields: {
                                 not_overridden_fields}")


class Link:
    """
    Defines a subclass to manage many-to-many relationship tables,
    ensuring a specific order of data loading.

    This class is intended to be used as a base for creating data models
    that represent many-to-many relationships. It includes mechanisms
    to define and enforce the order in which associated tables should be
    loaded into the database, facilitating correct data integrity and
    relationships between entities.
    """


@dataclass
class Genre(BaseModel):
    """
    Represents a genre categorizing film works.
    """

    schema: ClassVar[str] = 'content'
    table_name: ClassVar[str] = 'genre'
    constraints: ClassVar[List[str]] = ['id']
    retrieved_fields: ClassVar[List[str]] = ['id', 'name', 'description']

    name: str
    description: str
    id: uuid.UUID = field(default_factory=lambda: uuid.uuid4)
    created_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(
            tz=datetime.UTC))
    updated_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(
            tz=datetime.UTC))


@dataclass
class FilmWork(BaseModel):
    """
    Represents a film work in the database.
    """
    schema: ClassVar[str] = 'content'
    table_name: ClassVar[str] = 'film_work'
    constraints: ClassVar[List[str]] = ['id']
    retrieved_fields: ClassVar[List[str]] = ['id',
                                             'title',
                                             'description',
                                             'creation_date',
                                             'type',
                                             'file_path',
                                             'rating']

    title: str
    description: str
    creation_date: date
    type: str
    file_path: str
    rating: float = field(default_factory=0.0)
    id: uuid.UUID = field(default_factory=lambda: uuid.uuid4)
    created_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(
            tz=datetime.UTC))
    updated_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(
            tz=datetime.UTC))


@dataclass
class Person(BaseModel):
    """
    Represents a person involved in film works, such as actors or directors.
    """
    schema: ClassVar[str] = 'content'
    table_name: ClassVar[str] = 'person'
    constraints: ClassVar[List[str]] = ['id']
    retrieved_fields: ClassVar[List[str]] = ['id', 'full_name']

    full_name: str
    id: uuid.UUID = field(default_factory=lambda: uuid.uuid4)
    created_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(
            tz=datetime.UTC))
    updated_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(
            tz=datetime.UTC))


@dataclass
class PersonFilmWork(BaseModel, Link):
    """
    Represents a many-to-many relationship between persons and film works, indicating roles.
    """
    schema: ClassVar[str] = 'content'
    table_name: ClassVar[str] = 'person_film_work'
    constraints: ClassVar[List[str]] = ['id', 'person_id', 'film_work_id']
    retrieved_fields: ClassVar[List[str]] = [
        'id', 'person_id', 'film_work_id', 'role']

    role: str
    id: uuid.UUID = field(default_factory=lambda: uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=lambda: uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=lambda: uuid.uuid4)
    created_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(
            tz=datetime.UTC))


@dataclass
class GenreFilmWork(BaseModel, Link):
    """
    Represents a many-to-many relationship between genres and film works.
    """
    schema: ClassVar[str] = 'content'
    table_name: ClassVar[str] = 'genre_film_work'
    constraints: ClassVar[List[str]] = ['genre_id', 'film_work_id']
    retrieved_fields: ClassVar[List[str]] = ['id', 'genre_id', 'film_work_id']

    id: uuid.UUID = field(default_factory=lambda: uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=lambda: uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=lambda: uuid.uuid4)
    created_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(
            tz=datetime.UTC))
