from pydantic import Field

from etl_service.models.mixins import IdMixin, NameMixin


class Genre(IdMixin, NameMixin):
    """Defines genre model"""

    description: str | None = Field(None)
