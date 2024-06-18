from typing import Any, Protocol, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)
P = TypeVar("P", bound=Any, covariant=True)


class UserAuthenticationProtocol(Protocol[T, P]):
    async def user_login(self, request: Any, user: Any, permissions: Any) -> None:
        """User login."""
        raise NotImplementedError

    async def user_logout(self) -> None:
        """User logout."""
        raise NotImplementedError

    async def token_refresh(self) -> None:
        """Get new access and refresh tokens."""
        raise NotImplementedError

    async def login_history(self) -> list[T]:
        """Get user's login history."""
        raise NotImplementedError
