from datetime import datetime
from zoneinfo import ZoneInfo
from uuid import UUID

from pydantic import BaseModel


class IdMixin(BaseModel):
    """Mixin that adds a UUID primary key field to a model."""

    id: UUID


class UpdatedAtMixin(BaseModel):
    """Mixin that adds timestamp fields to a model, recording creation and last modification times."""

    updated_at: datetime = datetime.now(tz=ZoneInfo("UTC"))
