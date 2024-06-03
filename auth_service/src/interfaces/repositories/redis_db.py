from typing import Any

from auth_service.src.interfaces.repositories.base import RepositoryProtocol


class RedisRepositoryProtocol(RepositoryProtocol[str, Any, Any, str]):
    pass
