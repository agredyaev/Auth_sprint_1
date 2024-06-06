from typing import Any, Sequence, TypeVar
from uuid import UUID

from auth_service.src.interfaces.repositories.postgres import PostgresRepositoryProtocol

T = TypeVar("T")
P = TypeVar("P", bound=Any)


class LoginHistoryRepositoryProtocol(PostgresRepositoryProtocol[T]):
    async def create_login_record(self, record_data: P) -> None:
        raise NotImplementedError

    async def get_login_record(self, record_id: UUID) -> T | None:
        raise NotImplementedError

    async def list_login_records(self, user_id: UUID) -> Sequence[T]:
        raise NotImplementedError
