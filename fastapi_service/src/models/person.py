from fastapi_service.src.models.mixins import IdMixin


class Person(IdMixin):
    """Defines person model"""

    full_name: str


