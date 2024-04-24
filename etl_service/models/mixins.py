from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class IdMixin(BaseModel):
    """Mixin that adds a UUID primary key field to a model."""
    id: UUID


class UpdatedAtMixin(BaseModel):
    """Mixin that adds timestamp fields to a model, recording creation and last modification times."""
    updated_at: datetime = datetime.now(tz=datetime.UTC)
