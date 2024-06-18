from typing import Sequence, Type

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from auth_service.src.interfaces.repositories.role_permission import RolePermissionRepositoryProtocol
from auth_service.src.models import Permission, RolePermission
from auth_service.src.repositories import PostgresRepository
from auth_service.src.schemas.request import (
    PermissionLevelList,
    RoleGetPermissions,
    RoleId,
    RolePermissionRowCreate,
    RolePermissionsList,
)
from auth_service.src.utils.combinations import create_combinations
from auth_service.src.utils.db_operations import execute_list_query


class RolePermissionRepository(RolePermissionRepositoryProtocol[RolePermission], PostgresRepository[RolePermission]):
    _model: Type[RolePermission] = RolePermission

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session)

    async def get_permissions_list(self, role_data: RoleGetPermissions) -> Sequence[Permission]:
        permission_alias = aliased(Permission)
        query = (
            select(permission_alias)
            .select_from(self._model)
            .join(permission_alias, self._model.permission_id == permission_alias.id)
            .where(self._model.role_id == role_data.role_id)
        )
        role_permissions: Sequence[Permission] = await execute_list_query(self.db_session, query)
        return role_permissions

    async def create_records(self, role_data: RolePermissionsList) -> Sequence[RolePermission]:
        values = create_combinations(model_with_list=role_data, combination_model=RolePermissionRowCreate)
        query = insert(self._model).values(values).returning(self._model)
        role_permissions: Sequence[RolePermission] = await execute_list_query(self.db_session, query)

        return role_permissions

    async def delete_records(self, role_data: RoleId) -> Sequence[RolePermission]:
        condition = self._model.role_id == role_data.role_id
        delete_query = delete(self._model).where(condition).returning(self._model)
        role_permissions: Sequence[RolePermission] = await execute_list_query(self.db_session, delete_query)

        return role_permissions

    async def get_records(self, role_data: RoleId) -> Sequence[RolePermission]:
        query = select(self._model).where(self._model.role_id == role_data.role_id)
        role_permissions: Sequence[RolePermission] = await execute_list_query(self.db_session, query)

        return role_permissions

    async def get_permissions_ids(self, role_data: PermissionLevelList) -> Sequence[Permission]:
        query = (
            select(Permission)
            .select_from(Permission)
            .join(self._model, self._model.permission_id == Permission.id)
            .where(Permission.level.in_([level.level for level in role_data.permission_levels]))
        ).distinct()

        permissions: Sequence[Permission] = await execute_list_query(self.db_session, query)
        return permissions
