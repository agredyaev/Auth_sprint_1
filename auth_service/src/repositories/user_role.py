from typing import Sequence, Type

from sqlalchemy import and_, delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.src.core.logger import setup_logging
from auth_service.src.interfaces.repositories import UserRoleRepositoryProtocol
from auth_service.src.models import Role, User, UserRole
from auth_service.src.repositories.postgres import PostgresRepository
from auth_service.src.schemas.request import (
    UserGetRolePermissions,
    UserRoleAssign,
    UserRoleCreate,
    UserRoleRevoke,
    UserRoleVerify,
)
from auth_service.src.utils.combinations import create_combinations
from auth_service.src.utils.db_operations import execute_list_query

logger = setup_logging(__name__)


class UserRoleRepository(UserRoleRepositoryProtocol[UserRole], PostgresRepository[UserRole]):
    """Implementation of UserRoleRepositoryProtocol."""

    _model: Type[UserRole] = UserRole

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session)
        self.db_session = db_session

    async def create_records(self, user_data: UserRoleAssign) -> Sequence[UserRole]:
        values = create_combinations(user_data, UserRoleCreate)
        query = insert(self._model).values(values).returning(self._model)
        user_roles: Sequence[UserRole] = await execute_list_query(self.db_session, query)

        return user_roles

    async def delete_records(self, user_data: UserRoleRevoke) -> Sequence[UserRole]:
        roles = [role.role_id for role in user_data.roles]
        condition = and_(self._model.user_id == user_data.user_id, self._model.role_id.in_(roles))
        delete_query = delete(self._model).where(condition).returning(self._model)
        user_roles: Sequence[UserRole] = await execute_list_query(self.db_session, delete_query)

        return user_roles

    async def get_records(self, user_data: UserGetRolePermissions) -> Sequence[UserRole]:
        query = select(self._model).where(self._model.user_id == user_data.user_id)
        user_roles: Sequence[UserRole] = await execute_list_query(self.db_session, query)

        return user_roles

    async def check_records(self, user_data: UserRoleVerify) -> Sequence[UserRole]:
        query = (
            select(self._model)
            .join(User, self._model.user_id == User.id)
            .join(Role, self._model.role_id == Role.id)
            .where(User.email == user_data.email)
            .where(Role.name.in_([role.name for role in user_data.role_names]))
        )

        user_roles: Sequence[UserRole] = await execute_list_query(self.db_session, query)

        return user_roles
