from typing import Any, TypeVar

from auth_service.src.interfaces.repositories.postgres import PostgresRepositoryProtocol

T = TypeVar("T")
P = TypeVar("P", bound=Any)


class UserRepositoryProtocol(PostgresRepositoryProtocol[T]):
    async def create_user(self, user_data: P) -> T:
        """Create user."""
        raise NotImplementedError

    async def get_user_by_id(self, user_data: P) -> T | None:
        """Get user by id."""
        raise NotImplementedError

    async def get_user_by_email(self, user_data: P) -> T | None:
        """Get user by email."""
        raise NotImplementedError
