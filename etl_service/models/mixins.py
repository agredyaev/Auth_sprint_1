from datetime import datetime

from pydantic import BaseModel


class IdMixin(BaseModel):
    """Mixin that adds a UUID primary key field to a model."""

    id: str


class UpdatedAtMixin(BaseModel):
    """Mixin that adds timestamp fields to a model, recording creation and last modification times."""

    updated_at: datetime | str
