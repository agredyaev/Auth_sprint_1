from typing import Any, Sequence, TypeVar
from uuid import UUID

from auth_service.src.interfaces.repositories.postgres import PostgresRepositoryProtocol

T = TypeVar("T")
P = TypeVar("P", bound=Any)


class LoginHistoryRepositoryProtocol(PostgresRepositoryProtocol[T]):
    async def create_login_record(self, record_data: P) -> T:
        """Create login record."""
        raise NotImplementedError

    async def get_login_record(self, record_id: UUID) -> T | None:
        """Get login record by id."""
        raise NotImplementedError

    async def list_login_records(self, user_id: UUID) -> Sequence[T]:
        """List login records."""
        raise NotImplementedError

    async def update_login_record(self, record_data: P) -> T:
        """Update login record."""
        raise NotImplementedError
