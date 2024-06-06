from sqlalchemy.orm import Mapped, mapped_column

from auth_service.src.core.config import settings
from auth_service.src.models.base import STR_255, Base
from auth_service.src.models.mixins import CreatedAtMixin, IdMixin, LoginTimeMixin, LogoutTimeMixin, UserIdMixin


class LoginHistory(Base, IdMixin, UserIdMixin, CreatedAtMixin, LoginTimeMixin, LogoutTimeMixin):
    __tablename__ = "login_history"
    __table_args__ = {"schema": settings.pg.db_schema}

    user_agent: Mapped[STR_255] = mapped_column(nullable=False)
