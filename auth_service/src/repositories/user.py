from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.src.interfaces.repositories import UserRepositoryProtocol
from auth_service.src.models import User
from auth_service.src.repositories.postgres import PostgresRepository
from auth_service.src.schemas.request import UserCreate
from auth_service.src.schemas.request.user import UserGetByEmail, UserGetById
from auth_service.src.utils.db_operations import execute_single_query


class UserRepository(UserRepositoryProtocol[User], PostgresRepository[User]):
    """Implementation of UserRepositoryProtocol"""

    _model: Type[User] = User

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session)
        self.db_session = db_session

    async def create_user(self, user_data: UserCreate) -> User:
        user = await self.create(user_data)

        return user

    async def get_user_by_id(self, user_data: UserGetById) -> User | None:
        user = await self.get(user_data.id)

        return user

    async def get_user_by_email(self, user_data: UserGetByEmail) -> User | None:
        query = select(self._model).filter(self._model.email == user_data.email)
        user: User | None = await execute_single_query(self.db_session, query)

        return user
