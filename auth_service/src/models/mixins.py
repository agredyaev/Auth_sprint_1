from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from auth_service.src.core.config import settings
from auth_service.src.models.base import DATETIME_WITH_TIMEZONE, STR_255
from auth_service.src.utils import get_timestamp


class BaseMixin:
    __slots__ = ()
    __abstract__ = True


class IdMixin(BaseMixin):
    """Mixin that adds a UUID primary key field to a model."""

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, nullable=False)


class CreatedAtMixin(BaseMixin):
    """Mixin that adds a timestamp field to a model."""

    created_at: Mapped[DATETIME_WITH_TIMEZONE] = mapped_column(default=get_timestamp, nullable=False)


class UpdatedAtMixin(BaseMixin):
    """Mixin that adds a timestamp field to a model."""

    updated_at: Mapped[DATETIME_WITH_TIMEZONE] = mapped_column(
        default=get_timestamp, onupdate=get_timestamp, nullable=False
    )


class UserIdMixin(BaseMixin):
    """Mixin that adds a UUID primary key field to a model."""

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(column=f"{settings.pg.db_schema}.user.id", ondelete="CASCADE"), nullable=False
    )


class LoginTimeMixin:
    """Mixin that adds a timestamp field to a model."""

    login_at: Mapped[DATETIME_WITH_TIMEZONE] = mapped_column(default=get_timestamp)


class LogoutTimeMixin:
    """Mixin that adds a timestamp field to a model."""

    logout_at: Mapped[DATETIME_WITH_TIMEZONE] = mapped_column(nullable=True)


class NameMixin:
    """Mixin that adds a name field to a model."""

    name: Mapped[STR_255] = mapped_column(nullable=False)


class DescriptionMixin:
    """Mixin that adds a description field to a model."""

    description: Mapped[STR_255] = mapped_column(nullable=True)


class RoleIdMixin:
    """Mixin that adds a UUID primary key field to a model."""

    role_id: Mapped[UUID] = mapped_column(
        ForeignKey(column=f"{settings.pg.db_schema}.role.id", ondelete="CASCADE"), nullable=False
    )
