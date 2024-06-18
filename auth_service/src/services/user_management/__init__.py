from functools import lru_cache
from typing import Annotated, Any

from fastapi import Depends

from auth_service.src.interfaces.services import UserManagementProtocol
from auth_service.src.models import RolePermission, User, UserRole
from auth_service.src.repositories import (
    RolePermissionRepositoryProtocol,
    UserRepositoryProtocol,
    UserRoleRepositoryProtocol,
    get_role_permission_repository,
    get_user_repository,
    get_user_role_repository,
)
from auth_service.src.services.user_management.service import UserManagementService

__all__ = ["get_user_management_service"]


@lru_cache()
def get_user_management_service(
    user_repo: Annotated[UserRepositoryProtocol[User], Depends(get_user_repository)],
    user_role_repo: Annotated[UserRoleRepositoryProtocol[UserRole], Depends(get_user_role_repository)],
    role_permission_repo: Annotated[
        RolePermissionRepositoryProtocol[RolePermission], Depends(get_role_permission_repository)
    ],
) -> UserManagementProtocol[Any, Any]:
    """
    Provider for UserRegistrationService
    """
    return UserManagementService(
        user_repo=user_repo, user_role_repo=user_role_repo, role_permission_repo=role_permission_repo
    )
