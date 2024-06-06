from typing import Any, Sequence, TypeVar
from uuid import UUID

from auth_service.src.interfaces.repositories.postgres import PostgresRepositoryProtocol

T = TypeVar("T")
P = TypeVar("P", bound=Any)


class RoleRepositoryProtocol(PostgresRepositoryProtocol[T]):
    async def create_role(self, role_data: P) -> None:
        raise NotImplementedError

    async def get_role(self, role_id: UUID) -> T | None:
        raise NotImplementedError

    async def update_role(self, role_data: P) -> None:
        raise NotImplementedError

    async def delete_role(self, role_id: UUID) -> None:
        raise NotImplementedError

    async def list_roles(self) -> Sequence[T]:
        raise NotImplementedError
