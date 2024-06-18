from typing import Any, Sequence
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from starlette import status

from auth_service.src.interfaces.repositories import RolePermissionRepositoryProtocol, RoleRepositoryProtocol
from auth_service.src.interfaces.services import RoleManagementProtocol
from auth_service.src.models import Permission, Role, RolePermission
from auth_service.src.repositories.exceptions import NotFoundError
from auth_service.src.schemas.request import (
    RoleCreate,
    RoleDelete,
    RoleGetPermissions,
    RoleId,
    RolePermissionCreate,
    RolePermissionsList,
    RolePermissionUpdate,
)
from auth_service.src.schemas.request.role import PermissionLevelList, PermissionLevelSpec, RoleUpdate
from auth_service.src.schemas.request.role_permissions import PermissionId
from auth_service.src.schemas.response import RoleCreateResponse
from auth_service.src.schemas.response.role import (
    PermissionResponse,
    RoleDeleteResponse,
    RoleListResponse,
    RoleUpdateResponse,
)


class RoleManagementService(RoleManagementProtocol[Any, Any]):
    """Implementation of RoleManagementProtocol"""

    def __init__(
        self,
        role_repo: RoleRepositoryProtocol[Role],
        role_permission_repo: RolePermissionRepositoryProtocol[RolePermission],
    ):
        self.role_repo = role_repo
        self.role_permission_repo = role_permission_repo

    async def _process_permissions_by_level(
        self, role_id: UUID, permission_levels: list[PermissionLevelSpec]
    ) -> Sequence[Permission]:
        permissions = await self.role_permission_repo.get_permissions_ids(
            role_data=PermissionLevelList(permission_levels=permission_levels)
        )
        await self.role_permission_repo.create_records(
            role_data=RolePermissionsList(
                role_id=role_id,
                permissions=[PermissionId(permission_id=permission.id) for permission in permissions],
            )
        )
        return permissions

    async def create_role(self, role_data: RolePermissionCreate) -> RoleCreateResponse:
        try:
            role = await self.role_repo.create_role(RoleCreate(name=role_data.name, description=role_data.description))

        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Role {role_data.name} already exists")

        permissions = await self._process_permissions_by_level(
            role_id=role.id, permission_levels=role_data.permission_levels
        )

        return RoleCreateResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            permissions=[PermissionResponse(id=permission.id, name=permission.name) for permission in permissions],
        )

    async def delete_role(self, role_data: RoleDelete) -> RoleDeleteResponse:
        try:
            role = await self.role_repo.delete_role(role_id=role_data.id)
        except NotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role {role_data.id} not found")

        return RoleDeleteResponse(id=role.id, name=role.name, description=role.description)

    async def update_role(self, role_data: RolePermissionUpdate) -> RoleUpdateResponse:
        try:
            role = await self.role_repo.update_role(
                role_data=RoleUpdate(id=role_data.id, name=role_data.name, description=role_data.description)
            )
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role {role_data.id} not found")

        await self.role_permission_repo.delete_records(role_data=RoleId(role_id=role.id))
        permissions = await self._process_permissions_by_level(
            role_id=role.id, permission_levels=role_data.permission_levels
        )

        return RoleUpdateResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            permissions=[PermissionResponse(id=permission.id, name=permission.name) for permission in permissions],
        )

    async def list_roles(self) -> Sequence[RoleListResponse]:
        roles = await self.role_repo.list_roles()
        result = []

        for role in roles:
            permissions = await self.role_permission_repo.get_permissions_list(
                role_data=RoleGetPermissions(role_id=role.id)
            )
            result.append(
                RoleListResponse(
                    id=role.id,
                    created_at=role.created_at,
                    updated_at=role.updated_at,
                    name=role.name,
                    description=role.description,
                    permissions=[
                        PermissionResponse(id=permission.id, name=permission.name) for permission in permissions
                    ],
                )
            )

        return result
