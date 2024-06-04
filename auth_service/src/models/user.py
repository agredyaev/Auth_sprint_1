from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from auth_service.src.core.config import settings
from auth_service.src.models.base import STR_50, STR_255, STR_512, Base
from auth_service.src.models.mixins import CreatedAtMixin, IdMixin, UpdatedAtMixin, UserIdMixin


class User(Base, IdMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "user"
    __table_args__ = {"schema": settings.pg.db_schema}

    login: Mapped[STR_255] = mapped_column(unique=True, nullable=False)
    password: Mapped[STR_512] = mapped_column(nullable=False)
    first_name: Mapped[STR_50] = mapped_column(nullable=True)
    last_name: Mapped[STR_50] = mapped_column(nullable=True)


class UserRole(Base, UserIdMixin, CreatedAtMixin):
    __tablename__ = "user_role"
    __table_args__ = {"schema": settings.pg.db_schema}

    role_id: Mapped[UUID] = mapped_column(ForeignKey(column=f"{settings.pg.db_schema}.role.id"), nullable=False)
