from sqlalchemy import UniqueConstraint

from auth_service.src.core.config import settings
from auth_service.src.models.base import Base
from auth_service.src.models.mixins import CreatedAtMixin, DescriptionMixin, IdMixin, NameMixin, UpdatedAtMixin


class Role(Base, IdMixin, NameMixin, DescriptionMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "role"
    __table_args__ = (
        UniqueConstraint("name", name="unique_role_name"),
        {"schema": settings.pg.db_schema},
    )
