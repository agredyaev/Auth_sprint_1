from typing import Sequence, Type
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.src.interfaces.repositories import LoginHistoryRepositoryProtocol
from auth_service.src.models import LoginHistory
from auth_service.src.repositories.postgres import PostgresRepository
from auth_service.src.schemas.request import LoginHistoryCreate, LoginHistoryLogout
from auth_service.src.utils.db_operations import execute_list_query


class LoginHistoryRepository(LoginHistoryRepositoryProtocol[LoginHistory], PostgresRepository[LoginHistory]):
    _model: Type[LoginHistory] = LoginHistory

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session)

    async def create_login_record(self, record_data: LoginHistoryCreate) -> LoginHistory:
        return await self.create(record_data)

    async def get_login_record(self, record_id: UUID) -> LoginHistory | None:
        return await self.get(record_id)

    async def list_login_records(self, user_id: UUID) -> Sequence[LoginHistory]:
        query = select(self._model).filter(self._model.user_id == user_id)
        return await execute_list_query(self.db_session, query)

    async def update_login_record(self, record_data: LoginHistoryLogout) -> LoginHistory:
        return await self.merge(record_data)
