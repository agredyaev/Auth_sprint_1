from typing import Sequence, Type
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.src.core.logger import setup_logging
from auth_service.src.interfaces.repositories import RoleRepositoryProtocol
from auth_service.src.models import Role
from auth_service.src.repositories.exceptions import NotFoundError
from auth_service.src.repositories.postgres import PostgresRepository
from auth_service.src.schemas.request import RoleCreate, RoleUpdate
from auth_service.src.utils.db_operations import execute_single_query

logger = setup_logging(logger_name=__name__)


class RoleRepository(RoleRepositoryProtocol[Role], PostgresRepository[Role]):
    """
    Implementation of RoleRepositoryProtocol
    """

    _model: Type[Role] = Role

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session)

    async def create_role(self, role_data: RoleCreate) -> Role:
        return await self.create(role_data)

    async def get_role(self, role_id: UUID) -> Role | None:
        return await self.get(role_id)

    async def update_role(self, role_data: RoleUpdate) -> Role:
        return await self.merge(role_data)

    async def delete_role(self, role_id: UUID) -> Role:
        query = select(self._model).where(self._model.id == role_id)
        role: Role | None = await execute_single_query(self.db_session, query)
        if not role:
            logger.error(f"Role with id {role_id} not found")
            raise NotFoundError(f"Role with id {role_id} not found")
        await self.db_session.delete(role)
        return role

    async def list_roles(self) -> Sequence[Role]:
        return await self.list()
