from typing import Any, TypeVar

from auth_service.src.interfaces.repositories.postgres import PostgresRepositoryProtocol

T = TypeVar("T")
P = TypeVar("P", bound=Any)


class UserRoleRepositoryProtocol(PostgresRepositoryProtocol[T]):
    async def assign_role(self, user_role_data: P) -> None:
        raise NotImplementedError

    async def revoke_role(self, user_role_data: P) -> None:
        raise NotImplementedError
