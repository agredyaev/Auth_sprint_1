from typing import Any, Coroutine, Protocol, Sequence, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel, covariant=True)
P = TypeVar("P", bound=Any, contravariant=True)


class RoleManagementProtocol(Protocol[T, P]):
    def create_role(self, role_data: P) -> Coroutine[Any, Any, T]:
        """Create role"""
        raise NotImplementedError

    def delete_role(self, role_data: P) -> Coroutine[Any, Any, T]:
        """Delete role"""
        raise NotImplementedError

    def update_role(self, role_data: P) -> Coroutine[Any, Any, T]:
        """Update role"""
        raise NotImplementedError

    def list_roles(self) -> Coroutine[Any, Any, Sequence[T]]:
        """List roles"""
        raise NotImplementedError
