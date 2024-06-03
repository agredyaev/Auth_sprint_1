from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from auth_service.src.models.base import Base
from auth_service.src.models.mixins import DataType, IdMixin, LoginTimeMixin, LogoutTimeMixin, UserIdMixin, \
    CreatedAtMixin
from auth_service.src.core.config import settings


class LoginHistory(Base, IdMixin, UserIdMixin, LoginTimeMixin, LogoutTimeMixin, CreatedAtMixin):
    __tablename__ = "login_history"
    __table_args__ = {"schema": settings.pg.db_schema}

    user_agent: Mapped[DataType.STR_255] = mapped_column(String(255), nullable=False)
