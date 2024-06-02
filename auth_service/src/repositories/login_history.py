from typing import Sequence, TypeVar
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.src.core.logger import setup_logging
from auth_service.src.interfaces.repositories.login_history import LoginHistoryRepositoryProtocol
from auth_service.src.models.login_history import LoginHistory
from auth_service.src.repositories.postgres import PostgresRepository

T = TypeVar("T")

logger = setup_logging(logger_name=__name__)


class LoginHistoryRepository(LoginHistoryRepositoryProtocol[T], PostgresRepository[T]):
    _model = LoginHistory

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session)

    async def create_login_record(self, record_data: dict) -> None:
        return await self.create(record_data)

    async def get_login_record(self, record_id: UUID) -> T | None:
        return await self.get(record_id)

    async def list_login_records(self, user_id: UUID) -> Sequence[T]:
        return await self.list(user_id)
