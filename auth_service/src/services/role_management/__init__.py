from functools import lru_cache
from typing import Annotated, Any

from fastapi import Depends

from auth_service.src.interfaces.repositories import RolePermissionRepositoryProtocol, RoleRepositoryProtocol
from auth_service.src.interfaces.services.role_management import RoleManagementProtocol
from auth_service.src.models import Role, RolePermission
from auth_service.src.repositories import get_role_permission_repository, get_role_repository
from auth_service.src.services.role_management.service import RoleManagementService

__all__ = ["get_role_management_service", "RoleManagementProtocol"]


@lru_cache()
def get_role_management_service(
    role_repo: Annotated[RoleRepositoryProtocol[Role], Depends(get_role_repository)],
    role_permission_repo: Annotated[
        RolePermissionRepositoryProtocol[RolePermission], Depends(get_role_permission_repository)
    ],
) -> RoleManagementProtocol[Any, Any]:
    """
    Provider for RoleManagementService
    """
    return RoleManagementService(role_repo=role_repo, role_permission_repo=role_permission_repo)
