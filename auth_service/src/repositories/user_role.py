from typing import Type
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.src.core.logger import setup_logging
from auth_service.src.interfaces.repositories import UserRoleRepositoryProtocol
from auth_service.src.models import UserRole
from auth_service.src.repositories import PostgresRepository
from auth_service.src.schemas.request import UserRoleAssign, UserRoleRevoke
from auth_service.src.utils.db_operations import execute_single_query

logger = setup_logging(__name__)


class UserRoleRepository(UserRoleRepositoryProtocol[UserRole], PostgresRepository[UserRole]):
    """Implementation of UserRoleRepositoryProtocol."""

    _model: Type[UserRole] = UserRole

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session)
        self.db_session = db_session

    async def assign_role(self, user_data: UserRoleAssign) -> None:
        return await self.create(user_data)

    async def revoke_role(self, user_data: UserRoleRevoke) -> None:
        query = select(self._model).filter(
            self._model.user_id == user_data.user_id, self._model.role_id == user_data.role_id
        )
        user_role_id: UUID | None = await execute_single_query(self.db_session, query)
        if user_role_id is not None:
            return await self.delete(user_role_id)
        else:
            logger.error(
                f"Role assignment not found for the given user {user_data.user_id} and role {user_data.role_id} IDs."
            )
