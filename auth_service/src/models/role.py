from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from auth_service.src.core.config import settings
from auth_service.src.models.base import Base
from auth_service.src.models.mixins import DataType, IdMixin, NameMixin, CreatedAtMixin, UpdatedAtMixin


class Role(Base, IdMixin, NameMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "roles"
    _table_args__ = {"schema": settings.pg.db_schema}

    description: Mapped[DataType.STR_255] = mapped_column(String(255), nullable=True)
