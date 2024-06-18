from auth_service.src.interfaces.repositories.base import (
    CreateSchemaType,
    MergeSchemaType,
    RepositoryProtocol,
    UpdateSchemaType,
)
from auth_service.src.interfaces.repositories.login_history import LoginHistoryRepositoryProtocol
from auth_service.src.interfaces.repositories.postgres import PostgresRepositoryProtocol
from auth_service.src.interfaces.repositories.redis_db import RedisRepositoryProtocol
from auth_service.src.interfaces.repositories.role import RoleRepositoryProtocol
from auth_service.src.interfaces.repositories.role_permission import RolePermissionRepositoryProtocol
from auth_service.src.interfaces.repositories.token import TokenRepositoryProtocol
from auth_service.src.interfaces.repositories.user import UserRepositoryProtocol
from auth_service.src.interfaces.repositories.user_role import UserRoleRepositoryProtocol

__all__ = [
    "RepositoryProtocol",
    "LoginHistoryRepositoryProtocol",
    "RedisRepositoryProtocol",
    "PostgresRepositoryProtocol",
    "UserRepositoryProtocol",
    "UserRoleRepositoryProtocol",
    "RoleRepositoryProtocol",
    "CreateSchemaType",
    "UpdateSchemaType",
    "MergeSchemaType",
    "TokenRepositoryProtocol",
    "RolePermissionRepositoryProtocol",
]
