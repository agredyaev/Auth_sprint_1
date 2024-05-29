from typing import Protocol
from uuid import UUID
from auth_service.src.models.role import Role
from auth_service.src.utils.db_operations import execute_query
from sqlalchemy.ext.asyncio import AsyncSession


class RoleRetrievalProtocol(Protocol):
    async def get_role(self, role_id: UUID) -> Role | None:
        ...

    async def get_all_roles(self) -> list[Role]:
        ...


class RoleRetrievalService:
    """
    Implementation of RoleRetrievalProtocol
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_role(self, role_id: UUID) -> Role | None:
        result = await execute_query(self.db, select(Role).where(Role.id == role_id))
        return result.scalars().first()

    async def get_all_roles(self) -> list[Role]:
        result = await execute_query(self.db, select(Role))
        return result.scalars().all()
