from typing import Sequence, TypeVar
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.src.interfaces.repositories.role import RoleRepositoryProtocol
from auth_service.src.models.role import Role
from auth_service.src.repositories.postgres import PostgresRepository

T = TypeVar("T")


class RoleRepository(RoleRepositoryProtocol[T], PostgresRepository[T]):
    """
    Implementation of RoleRepositoryProtocol
    """

    _model = Role

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session)

    async def create_role(self, role_data: dict) -> None:
        return await self.create(role_data)

    async def get_role(self, role_id: UUID) -> T | None:
        return await self.get(role_id)

    async def update_role(self, role_id: UUID, role_data: dict) -> None:
        return await self.update(role_id, role_data)

    async def delete_role(self, role_id: UUID) -> None:
        return await self.delete(role_id)

    async def list_roles(self) -> Sequence[T]:
        return await self.list()
