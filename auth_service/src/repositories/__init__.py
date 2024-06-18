from functools import lru_cache
from typing import Annotated, Any

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.src.db import get_redis, get_session
from auth_service.src.interfaces.repositories import (
    LoginHistoryRepositoryProtocol,
    RolePermissionRepositoryProtocol,
    RoleRepositoryProtocol,
    TokenRepositoryProtocol,
    UserRepositoryProtocol,
    UserRoleRepositoryProtocol,
)
from auth_service.src.models import LoginHistory, RolePermission, User, UserRole
from auth_service.src.repositories.login_history import LoginHistoryRepository
from auth_service.src.repositories.postgres import PostgresRepository
from auth_service.src.repositories.redis_db import RedisRepository
from auth_service.src.repositories.role import RoleRepository
from auth_service.src.repositories.role_permission import RolePermissionRepository
from auth_service.src.repositories.token import TokenRepository
from auth_service.src.repositories.user import UserRepository
from auth_service.src.repositories.user_role import UserRoleRepository

__all__ = [
    "get_login_history_repository",
    "LoginHistoryRepository",
    "RedisRepository",
    "PostgresRepository",
    "UserRepository",
    "RoleRepository",
    "TokenRepository",
    "get_user_repository",
    "UserRepositoryProtocol",
    "get_user_role_repository",
    "UserRoleRepositoryProtocol",
    "get_token_repository",
    "TokenRepositoryProtocol",
    "get_role_permission_repository",
    "RolePermissionRepositoryProtocol",
    "get_role_repository",
    "RoleRepositoryProtocol",
]


@lru_cache()
def get_user_repository(
    db_session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRepositoryProtocol[User]:
    """
    Provider for UserRepository
    """
    return UserRepository(db_session=db_session)


@lru_cache()
def get_user_role_repository(
    db_session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRoleRepositoryProtocol[UserRole]:
    """
    Provider for UserRoleRepository
    """
    return UserRoleRepository(db_session=db_session)


@lru_cache()
def get_login_history_repository(
    db_session: Annotated[AsyncSession, Depends(get_session)],
) -> LoginHistoryRepositoryProtocol[LoginHistory]:
    """
    Provider for LoginHistoryRepository
    """
    return LoginHistoryRepository(db_session=db_session)


@lru_cache()
def get_role_permission_repository(
    db_session: Annotated[AsyncSession, Depends(get_session)],
) -> RolePermissionRepositoryProtocol[RolePermission]:
    """
    Provider for UserRoleRepository
    """
    return RolePermissionRepository(db_session=db_session)


@lru_cache()
def get_token_repository(
    redis: Annotated[Redis, Depends(get_redis)],
) -> TokenRepositoryProtocol[Any]:
    """
    Provider for TokenRepository
    """
    return TokenRepository(redis=redis)


@lru_cache()
def get_role_repository(
    db_session: Annotated[AsyncSession, Depends(get_session)],
) -> RoleRepositoryProtocol[Any]:
    """
    Provider for TokenRepository
    """
    return RoleRepository(db_session=db_session)
