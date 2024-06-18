from typing import Any, Sequence, TypeVar

from auth_service.src.interfaces.repositories.postgres import PostgresRepositoryProtocol

T = TypeVar("T")
P = TypeVar("P", bound=Any)


class RolePermissionRepositoryProtocol(PostgresRepositoryProtocol[T]):
    async def get_permissions_list(self, role_data: P) -> Sequence[Any]:
        raise NotImplementedError

    async def create_records(self, role_data: P) -> Sequence[Any]:
        """
        Create new roles permissions.
        """
        raise NotImplementedError

    async def delete_records(self, role_data: P) -> Sequence[Any]:
        """
        Delete role permissions.
        """
        raise NotImplementedError

    async def get_records(self, role_data: P) -> Sequence[Any]:
        """
        Get role permissions.
        """
        raise NotImplementedError

    async def get_permissions_ids(self, role_data: P) -> Sequence[Any]:
        raise NotImplementedError
