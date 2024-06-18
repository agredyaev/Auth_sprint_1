from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from auth_service.src.core.config import settings
from auth_service.src.models.base import Base
from auth_service.src.models.mixins import CreatedAtMixin, IdMixin, RoleIdMixin


class RolePermission(Base, IdMixin, RoleIdMixin, CreatedAtMixin):
    __tablename__ = "role_permission"
    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="unique_role_permission"),
        {"schema": settings.pg.db_schema},
    )
    permission_id: Mapped[UUID] = mapped_column(
        ForeignKey(column=f"{settings.pg.db_schema}.permission.id", ondelete="CASCADE"), nullable=False
    )
