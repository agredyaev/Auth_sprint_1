from typing import Any, Coroutine, Protocol, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel, covariant=True)
P = TypeVar("P", bound=Any, contravariant=True)


class AuthJWTProtocol(Protocol[T, P]):
    def generate_tokens(self, current_user: Any, fresh: bool) -> Coroutine[Any, Any, T]:
        """Create access and refresh tokens."""
        raise NotImplementedError

    def set_cookies(self, obj_in: P) -> Coroutine[Any, Any, None]:
        """Set cookies."""
        raise NotImplementedError

    def unset_cookies(self) -> Coroutine[Any, Any, None]:
        """Unset cookies."""
        raise NotImplementedError

    def get_jwt_subject_json(self) -> Coroutine[Any, Any, Any]:
        """Get JWT subject (payload) JSON."""
        raise NotImplementedError

    def get_tokens_jti(self) -> Coroutine[Any, Any, T]:
        """Get token ID (JTI)."""
        raise NotImplementedError

    def extract_jti(self, encoded_token: str) -> Coroutine[Any, Any, str]:
        """Get token ID (JTI)."""
        raise NotImplementedError
