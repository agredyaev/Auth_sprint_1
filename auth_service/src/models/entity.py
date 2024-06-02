import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Table, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from auth_service.src.db.postgres import Base


class UUIDMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)


class UserIdMixin:
    __slot__ = ("user_id",)

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="users.id"), nullable=False
    )


UsersRoles = Table(
    "users_roles",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("users.id"), primary_key=True),
    Column("role_id", UUID, ForeignKey("roles.id"), primary_key=True),
)


class Users(UUIDMixin, Base):
    __tablename__ = "users"

    login = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    roles = relationship("Roles", secondary=UsersRoles, back_populates="users")
    login_history = relationship("LoginHistory", back_populates="users")

    def __init__(self, login: str, password: str, first_name: str, last_name: str) -> None:
        self.login = login
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f"<User {self.login}>"


class Roles(UUIDMixin, Base):
    __tablename__ = "roles"

    name = Column(String, nullable=False)

    users = relationship("Users", secondary=UsersRoles, back_populates="roles")

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"<Role {self.name}>"


class LoginHistory(UUIDMixin, UserIdMixin, Base):
    __tablename__ = "login_history"

    time = Column(DateTime, server_default=func.now())
    user_agent = Column(String)

    users = relationship("Users", back_populates="login_history")

    def __init__(self, id: uuid.uuid4) -> None:
        self.id = id

    def __repr__(self) -> str:
        return f"<LoginHistory {self.id}>"
