from uuid import UUID

from pydantic import BaseModel

from auth_service.src.schemas.mixins import RoleIdMixin


class PermissionId(BaseModel):
    permission_id: UUID


class RoleId(RoleIdMixin):
    pass


class RolePermissionsList(RoleIdMixin):
    permissions: list[PermissionId]


class RolePermissionSingle(RoleIdMixin, PermissionId):
    pass
