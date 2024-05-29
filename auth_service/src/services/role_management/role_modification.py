from typing import Protocol
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from auth_service.src.models.role import Role
from auth_service.src.schemas.role import RoleUpdate
from auth_service.src.utils.db_operations import add_and_commit, refresh_instance, delete_and_commit


class RoleModificationProtocol(Protocol):
    async def update_role(self, role_id: UUID, role: RoleUpdate) -> Role:
        ...

    async def delete_role(self, role_id: UUID) -> None:
        ...


class RoleModificationService:
    """
    Implementation of RoleModificationProtocol
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_role(self, role_id: UUID, role: RoleUpdate) -> Role:
        existing_role = await self.get_role(role_id)
        if not existing_role:
            handle_not_found("Role")
        for key, value in role.dict().items():
            setattr(existing_role, key, value)
        await add_and_commit(self.db, existing_role)
        await refresh_instance(self.db, existing_role)
        return existing_role

    async def delete_role(self, role_id: UUID) -> None:
        existing_role = await self.get_role(role_id)
        if not existing_role:
            handle_not_found("Role")
        await delete_and_commit(self.db, existing_role)
