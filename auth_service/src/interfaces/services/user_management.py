from typing import Any, Protocol, Sequence, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel, covariant=True)
P = TypeVar("P", bound=Any, contravariant=True)


class UserManagementProtocol(Protocol[T, P]):
    async def user_signup(self, obj_in: P) -> T:
        """User registration."""
        raise NotImplementedError

    async def update_password(self, obj_in: P) -> T:
        """User password update."""
        raise NotImplementedError

    async def check_password(self, obj_in: P) -> T:
        """User password check."""
        raise NotImplementedError

    async def assign_role(self, obj_in: P) -> T:
        """Assign role to user."""
        raise NotImplementedError

    async def revoke_role(self, obj_in: P) -> T:
        """Revoke role from user."""
        raise NotImplementedError

    async def verify_role(self, obj_in: P) -> T:
        """Verify users."""
        raise NotImplementedError

    async def get_user_permissions(self, obj_in: P) -> Sequence[Any]:
        """Get user permissions."""
        raise NotImplementedError
