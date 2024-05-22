from pydantic import BaseModel

from fastapi_service.src.models.mixins import IdMixin


class PersonFilmwork(BaseModel):
    """Defines person filmwork model"""

    id: str
    title: str
    roles: list[str]


class Person(IdMixin):
    """Defines person model"""

    full_name: str
    films: list[PersonFilmwork]
