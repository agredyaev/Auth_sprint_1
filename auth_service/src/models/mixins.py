from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from auth_service.src.core.config import settings
from auth_service.src.models.base import STR_255


def get_timestamp() -> datetime:
    """Get current timestamp."""
    return datetime.now(timezone.utc)


class IdMixin:
    """Mixin that adds a UUID primary key field to a model."""

    __slots__ = ()

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, nullable=False)


class CreatedAtMixin:
    """Mixin that adds a timestamp field to a model."""

    __slots__ = ()

    created_at: Mapped[datetime] = mapped_column(default=get_timestamp, nullable=False)


class UpdatedAtMixin:
    """Mixin that adds a timestamp field to a model."""

    __slots__ = ()

    updated_at: Mapped[datetime] = mapped_column(onupdate=get_timestamp, nullable=False)


class UserIdMixin:
    """Mixin that adds a UUID primary key field to a model."""

    __slots__ = ()

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(column=f"{settings.pg.db_schema}.user.id", ondelete="CASCADE"), nullable=False
    )


class LoginTimeMixin:
    """Mixin that adds a timestamp field to a model."""

    __slots__ = ()

    login_at: Mapped[datetime] = mapped_column(default=get_timestamp)


class LogoutTimeMixin:
    """Mixin that adds a timestamp field to a model."""

    __slots__ = ()

    logout_at: Mapped[datetime] = mapped_column(default=get_timestamp)


class NameMixin:
    """Mixin that adds a name field to a model."""

    __slots__ = ()

    name: Mapped[STR_255] = mapped_column(nullable=False)
