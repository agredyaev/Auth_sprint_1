import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash

from auth_service.src.db.postgres import Base


class UUIDMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())


class UserRole(CreatedAtMixin, Base):
    __tablename__ = "user_role"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="user.id", ondelete="CASCADE"), nullable=False, primary_key=True
    )
    role_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="role.id", ondelete="CASCADE"), nullable=False, primary_key=True
    )


class User(UUIDMixin, CreatedAtMixin, UpdatedAtMixin, Base):
    __tablename__ = "user"

    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)

    roles: Mapped[list["Role"]] = relationship(secondary="user_role")
    login_history: Mapped[list["LoginHistory"]] = relationship(back_populates="user")

    def __init__(self, login: str, password: str, first_name: str, last_name: str) -> None:
        self.login = login
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f"<User {self.login}>"


class Role(UUIDMixin, CreatedAtMixin, UpdatedAtMixin, Base):
    __tablename__ = "role"

    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    users: Mapped[list["User"]] = relationship(secondary="user_role")

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"<Role {self.name}>"


class LoginHistory(UUIDMixin, Base):
    __tablename__ = "login_history"

    user_id: Mapped[UUID] = mapped_column(ForeignKey(column="user.id", ondelete="CASCADE"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())
    user_agent: Mapped[str] = mapped_column()

    user: Mapped["User"] = relationship(back_populates="login_history")

    def __init__(self, id: uuid.uuid4, user_agent: str) -> None:
        self.id = id
        self.user_agent = user_agent

    def __repr__(self) -> str:
        return f"<LoginHistory {self.id}>"
