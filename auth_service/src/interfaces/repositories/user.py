from typing import Any, TypeVar
from uuid import UUID

from auth_service.src.interfaces.repositories.postgres import PostgresRepositoryProtocol

T = TypeVar("T")
P = TypeVar("P", bound=Any)


class UserRepositoryProtocol(PostgresRepositoryProtocol[T]):
    async def create_user(self, user_data: dict) -> T:
        raise NotImplementedError

    async def assign_role(self, user_id: UUID, role_id: UUID) -> None:
        raise NotImplementedError

    async def remove_role(self, user_id: UUID, role_id: UUID) -> None:
        raise NotImplementedError

    async def update_password(self, user_id: UUID, new_password: str) -> None:
        raise NotImplementedError
