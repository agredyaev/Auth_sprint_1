from fastapi_service.src.models.mixins import IdMixin


class Person(IdMixin):
    """Defines person model"""

    full_name: str


class FilmPerson(IdMixin):
    """Defines film person model"""

    title: str
    roles: list[str]
