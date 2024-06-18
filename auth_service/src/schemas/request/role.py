from uuid import UUID

from pydantic import BaseModel

from auth_service.src.core.default_user_roles import PermissionLevel
from auth_service.src.schemas.mixins import DescriptionMixin, IdMixin, NameMixin, RoleIdMixin


class PermissionLevelSpec(BaseModel):
    level: PermissionLevel


class RoleCreate(NameMixin, DescriptionMixin):
    pass


class RoleReCreate(IdMixin, NameMixin, DescriptionMixin):
    pass


class PermissionLevelList(BaseModel):
    permission_levels: list[PermissionLevelSpec]


class RolePermissionCreate(RoleCreate, PermissionLevelList):
    pass


class RolesCreate(BaseModel):
    roles: list[RoleCreate]


class RoleUpdate(IdMixin, RoleCreate):
    pass


class RolePermissionUpdate(IdMixin, RolePermissionCreate):
    pass


class RoleDelete(IdMixin):
    pass


class RoleGetPermissions(RoleIdMixin):
    pass


class RolePermissionRowCreate(BaseModel):
    role_id: UUID
    permission_id: UUID


class RoleIdFromPermission(RoleIdMixin):
    pass
