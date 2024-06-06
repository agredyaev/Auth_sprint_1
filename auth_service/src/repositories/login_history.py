from typing import Sequence, Type
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.src.interfaces.repositories import LoginHistoryRepositoryProtocol
from auth_service.src.models import LoginHistory
from auth_service.src.repositories import PostgresRepository
from auth_service.src.schemas.request import LoginHistoryCreate


class LoginHistoryRepository(LoginHistoryRepositoryProtocol[LoginHistory], PostgresRepository[LoginHistory]):
    _model: Type[LoginHistory] = LoginHistory

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session)

    async def create_login_record(self, record_data: LoginHistoryCreate) -> None:
        return await self.create(record_data)

    async def get_login_record(self, record_id: UUID) -> LoginHistory | None:
        return await self.get(record_id)

    async def list_login_records(self, user_id: UUID) -> Sequence[LoginHistory]:
        return await self.list(user_id)
