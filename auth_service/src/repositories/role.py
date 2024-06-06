from typing import Sequence, Type
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.src.interfaces.repositories import RoleRepositoryProtocol
from auth_service.src.models import Role
from auth_service.src.repositories import PostgresRepository
from auth_service.src.schemas.request import RoleCreate, RoleUpdate


class RoleRepository(RoleRepositoryProtocol[Role], PostgresRepository[Role]):
    """
    Implementation of RoleRepositoryProtocol
    """

    _model: Type[Role] = Role

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session)

    async def create_role(self, role_data: RoleCreate) -> None:
        return await self.create(role_data)

    async def get_role(self, role_id: UUID) -> Role | None:
        return await self.get(role_id)

    async def update_role(self, role_data: RoleUpdate) -> None:
        return await self.merge(role_data)

    async def delete_role(self, role_id: UUID) -> None:
        return await self.delete(role_id)

    async def list_roles(self) -> Sequence[Role]:
        return await self.list()
