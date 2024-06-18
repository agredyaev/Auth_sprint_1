from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from auth_service.src.core.config import settings
from auth_service.src.models.base import Base
from auth_service.src.models.mixins import CreatedAtMixin, DescriptionMixin, IdMixin, NameMixin, UpdatedAtMixin


class Permission(Base, IdMixin, NameMixin, DescriptionMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "permission"
    __table_args__ = (
        UniqueConstraint("name", name="unique_permission_name"),
        {"schema": settings.pg.db_schema},
    )

    level: Mapped[int] = mapped_column(default=0, nullable=False)
