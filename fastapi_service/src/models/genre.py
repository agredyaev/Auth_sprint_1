from fastapi_service.src.models.mixins import IdMixin, NameMixin
from pydantic import Field


class Genre(IdMixin, NameMixin):
    """Defines genre model"""

    description: str | None = Field("")
