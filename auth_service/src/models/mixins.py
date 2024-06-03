import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Annotated

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


def get_timestamp() -> datetime:
    """Get current timestamp."""
    return datetime.now(timezone.utc)


class DataType(Enum):
    STR_255 = Annotated[str, 255]
    STR_50 = Annotated[str, 50]


class IdMixin:
    """Mixin that adds a UUID primary key field to a model."""

    __slot__ = ("id",)

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
    )


class CreatedAtMixin:
    """Mixin that adds a timestamp field to a model."""

    __slot__ = ("created_at",)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=get_timestamp, nullable=False)


class UpdatedAtMixin:
    """Mixin that adds a timestamp field to a model."""

    __slot__ = ("modified_at",)

    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=get_timestamp, nullable=False)


class UserIdMixin:
    """Mixin that adds a UUID primary key field to a model."""

    __slot__ = ("user_id",)

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="users.id", ondelete="CASCADE"), primary_key=True, nullable=False
    )


class LoginTimeMixin:
    """Mixin that adds a timestamp field to a model."""

    __slot__ = ("login_time",)

    login_at: Mapped[datetime] = mapped_column(DateTime, default=get_timestamp)


class LogoutTimeMixin:
    """Mixin that adds a timestamp field to a model."""

    __slot__ = ("logout_time",)

    logout_at: Mapped[datetime] = mapped_column(DateTime, default=get_timestamp)


class NameMixin:
    """Mixin that adds a name field to a model."""

    __slot__ = ("name",)

    name: Mapped[DataType.STR_255] = mapped_column(String(255), nullable=False)
