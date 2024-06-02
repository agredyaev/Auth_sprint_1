import uuid

from auth_service.src.db.postgres import Base
from sqlalchemy import Column, DateTime, ForeignKey, String, Table, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

UsersRoles = Table(
    'users_roles',
    Base.metadata,
    Column('user_id', UUID, ForeignKey('users.id')),
    Column('role_id', UUID, ForeignKey('roles.id'))
)


class Users(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4,
                unique=True,
                nullable=False)
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
        return f'<User {self.login}>'


class Roles(Base):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4,
                unique=True,
                nullable=False)
    name = Column(String, nullable=False)

    users = relationship("Users", secondary=UsersRoles, back_populates="roles")

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'<Role {self.name}>'


class LoginHistory(Base):
    __tablename__ = 'login_history'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4,
                unique=True,
                nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    time = Column(DateTime, server_default=func.now())
    user_agent = Column(String)

    users = relationship("Users", back_populates="login_history")

    def __init__(self, id: uuid.uuid4) -> None:
        self.id = id

    def __repr__(self) -> str:
        return f'<LoginHistory {self.id}>'
