from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from auth_service.src.core.config import settings
from auth_service.src.models.base import Base
from auth_service.src.models.mixins import CreatedAtMixin, IdMixin, UserIdMixin


class UserRole(Base, IdMixin, UserIdMixin, CreatedAtMixin):
    __tablename__ = "user_role"
    __table_args__ = (
        UniqueConstraint('user_id', 'role_id', name='unique_user_role'),
        {"schema": settings.pg.db_schema},
    )
    role_id: Mapped[UUID] = mapped_column(
        ForeignKey(column=f"{settings.pg.db_schema}.role.id", ondelete="CASCADE"), nullable=False
    )
