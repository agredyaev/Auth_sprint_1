from typing import TypeVar
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import generate_password_hash

from auth_service.src.core.logger import setup_logging
from auth_service.src.interfaces.repositories.user import UserRepositoryProtocol
from auth_service.src.models import User, UserRole
from auth_service.src.repositories.postgres import PostgresRepository
from auth_service.src.utils.db_operations import (
    commit_to_db,
)

T = TypeVar("T")

logger = setup_logging(logger_name=__name__)


class UserRepository(UserRepositoryProtocol[T], PostgresRepository[T]):
    _model = User

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session)
        self.db_session = db_session

    async def create_user(self, user_data: dict) -> T:
        user = self._model(**user_data)
        await self.create(user)
        return user

    async def assign_role(self, user_id: UUID, role_id: UUID) -> None:
        role_data = {"user_id": user_id, "role_id": role_id}
        # TODO: check user role
        db_obj = UserRole.__table__(**role_data)
        await commit_to_db(self.db_session, db_obj, merge=True)

    async def revoke_role(self, user_id: UUID, role_id: UUID) -> None:
        query = UserRole.__table__.delete().where(UserRole.c.user_id == user_id).where(UserRole.c.role_id == role_id)
        async with self.db_session.begin():
            try:
                await self.db_session.execute(query)
                await self.db_session.commit()
            except SQLAlchemyError as e:
                logger.exception(msg="Failed to remove role:", exc_info=e)
                await self.db_session.rollback()
                raise e

    async def update_password(self, user_id: UUID, new_password: str) -> None:
        hashed_password = generate_password_hash(new_password)
        async with self.db_session.begin():
            try:
                await self.db_session.merge({"id": user_id, "password": hashed_password})
                await self.db_session.commit()
            except SQLAlchemyError as e:
                logger.exception(msg="Failed to update password:", exc_info=e)
                await self.db_session.rollback()
                raise e
