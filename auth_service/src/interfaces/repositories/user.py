from typing import Any, TypeVar

from auth_service.src.interfaces.repositories.postgres import PostgresRepositoryProtocol

T = TypeVar("T")
P = TypeVar("P", bound=Any)


class UserRepositoryProtocol(PostgresRepositoryProtocol[T]):
    async def create_user(self, user_data: P) -> None:
        raise NotImplementedError

    async def update_password(self, user_data: P) -> None:
        raise NotImplementedError
