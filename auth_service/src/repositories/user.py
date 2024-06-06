from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.src.interfaces.repositories import UserRepositoryProtocol
from auth_service.src.models import User
from auth_service.src.repositories import PostgresRepository
from auth_service.src.schemas.request import UserCreate, UserUpdate


class UserRepository(UserRepositoryProtocol[User], PostgresRepository[User]):
    """Implementation of UserRepositoryProtocol"""

    _model: Type[User] = User

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session)
        self.db_session = db_session

    async def create_user(self, user_data: UserCreate) -> None:
        return await self.create(user_data)

    async def update_password(self, user_data: UserUpdate) -> None:
        return await self.merge(user_data)
