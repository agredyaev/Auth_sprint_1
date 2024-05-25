import hashlib
from typing import Any, Awaitable, Callable

import orjson

from fastapi_service.src.core.config import settings
from fastapi_service.src.db.redis import get_redis

redis_client = get_redis


class BaseCacheService:
    """
    Base class for cache services.
    """

    @staticmethod
    async def fetch_from_cache(key: str) -> dict[str, Any] | None:
        """
        Retrieve cached data by key.

        :param key: cache key
        :return: cached data
        """
        adapter = await redis_client()
        data = await adapter.get(key)
        if not data:
            return None
        return orjson.loads(data)

    @staticmethod
    async def store_in_cache(key: str, data: str) -> None:
        """
        Store data in the cache with a key.

        :param key: cache key
        :param data: data to store
        """
        adapter = await redis_client()
        await adapter.set(key, data, settings.redis.cache_expiration)

    async def cached_result(
        self, cache_key: str, func: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any
    ) -> Any:
        result = await self.fetch_from_cache(cache_key)
        if not result:
            result = await func(*args, **kwargs)
            if not result:
                return None
            await self.store_in_cache(cache_key, orjson.dumps(result).decode("utf-8"))
        return result


class ModelCacheDecorator(BaseCacheService):
    """Decorator that caches model data for database queries."""

    def __init__(self, *, key: str = ""):
        self.key = key

    def __call__(self, func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            cache_key = kwargs.get(self.key)
            if not cache_key:
                cache_key = "".join(tuple(kwargs.values()))

            hasher = hashlib.sha256()
            hasher.update(bytes(cache_key, "utf-8"))
            cache_key = hasher.hexdigest()

            return await self.cached_result(cache_key, func, *args, **kwargs)

        return wrapper


class QueryCacheDecorator(BaseCacheService):
    """Decorator that caches query results."""

    def __call__(self, func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            hasher = hashlib.sha256()
            for arg in kwargs.values():
                hasher.update(bytes(str(arg), "utf-8"))
            cache_key = hasher.hexdigest()

            return await self.cached_result(cache_key, func, *args, **kwargs)

        return wrapper
