from sqlalchemy.orm import Mapped, mapped_column

from auth_service.src.core.config import settings
from auth_service.src.models.base import STR_255, Base
from auth_service.src.models.mixins import CreatedAtMixin, IdMixin, NameMixin, UpdatedAtMixin


class Role(Base, IdMixin, NameMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "role"
    __table_args__ = {"schema": settings.pg.db_schema}

    description: Mapped[STR_255] = mapped_column(nullable=True)
