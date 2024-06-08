from typing import Any, Coroutine, Protocol, TypeVar

from auth_service.src.schemas.response import TokensResponse

T = TypeVar("T", bound=Any)


class AuthJWTProtocol(Protocol):
    def create_token(self, obj_in: T) -> Coroutine[Any, Any, TokensResponse]:
        raise NotImplementedError

    def refresh_token(self) -> Coroutine[Any, Any, TokensResponse]:
        raise NotImplementedError

    def revoke_token(self, obj_in: T) -> Coroutine[Any, Any, None]:
        raise NotImplementedError
