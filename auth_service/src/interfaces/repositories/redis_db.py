from typing import Any, TypeVar

from auth_service.src.interfaces.repositories.base import RepositoryProtocol

T = TypeVar("T")


class RedisRepositoryProtocol(RepositoryProtocol[T, Any, Any, Any]):
    pass
