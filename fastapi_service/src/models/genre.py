from pydantic import Field

from fastapi_service.src.models.mixins import IdMixin, NameMixin


class Genre(IdMixin, NameMixin):
    """Defines genre model"""

    description: str | None = Field("")
