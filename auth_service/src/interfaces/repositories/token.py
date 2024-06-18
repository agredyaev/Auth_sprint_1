from typing import Any, TypeVar

from auth_service.src.interfaces.repositories.redis_db import RedisRepositoryProtocol

T = TypeVar("T")
P = TypeVar("P", bound=Any)


class TokenRepositoryProtocol(RedisRepositoryProtocol[T]):
    async def set_token(self, obj_in: P) -> None:
        raise NotImplementedError

    async def get_token(self, obj_in: P) -> Any | None:
        raise NotImplementedError
