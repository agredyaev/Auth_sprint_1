from typing import Any, Sequence, TypeVar

from auth_service.src.interfaces.repositories.postgres import PostgresRepositoryProtocol

T = TypeVar("T")
P = TypeVar("P", bound=Any)
Q = TypeVar("Q", bound=Any)


class UserRoleRepositoryProtocol(PostgresRepositoryProtocol[T]):
    async def create_records(self, user_data: P) -> Sequence[T]:
        """
        Create new user roles.
        """
        raise NotImplementedError

    async def delete_records(self, user_data: P) -> Sequence[T]:
        """
        Delete user roles.
        """
        raise NotImplementedError

    async def get_records(self, user_data: P) -> Sequence[T]:
        """
        Get user roles.
        """
        raise NotImplementedError

    async def check_records(self, user_data: P) -> Sequence[T]:
        """
        Check user roles.
        """
        raise NotImplementedError
