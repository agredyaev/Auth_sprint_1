from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from auth_service.src.core.config import settings
from auth_service.src.models.base import Base
from auth_service.src.models.mixins import IdMixin, CreatedAtMixin, UserIdMixin, DataType, UpdatedAtMixin


class User(Base, IdMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "users"
    _table_args__ = {"schema": settings.pg.db_schema}

    login: Mapped[DataType.STR_255] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[DataType.STR_50] = mapped_column(String(50), nullable=True)
    last_name: Mapped[DataType.STR_50] = mapped_column(String(50), nullable=True)


class UserRole(Base, UserIdMixin, CreatedAtMixin):
    __tablename__ = "user_roles"
    _table_args__ = {"schema": settings.pg.db_schema}

    role_id: Mapped[UUID] = mapped_column(ForeignKey(column="roles.id"), nullable=False)
