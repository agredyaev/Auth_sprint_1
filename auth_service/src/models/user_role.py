from sqlalchemy import UniqueConstraint

from auth_service.src.core.config import settings
from auth_service.src.models.base import Base
from auth_service.src.models.mixins import CreatedAtMixin, IdMixin, RoleIdMixin, UserIdMixin


class UserRole(Base, IdMixin, UserIdMixin, RoleIdMixin, CreatedAtMixin):
    __tablename__ = "user_role"
    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="unique_user_role"),
        {"schema": settings.pg.db_schema},
    )
