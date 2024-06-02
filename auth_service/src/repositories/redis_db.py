from typing import Any

from redis.asyncio import Redis
from redis.exceptions import RedisError

from auth_service.src.core.exceptions.redis import (
    RedisCreateError,
    RedisDeleteError,
    RedisGetError,
    RedisListError,
    RedisUpdateError,
)
from auth_service.src.core.logger import setup_logging
from auth_service.src.interfaces.repositories.redis_db import RedisRepositoryProtocol

logger = setup_logging(logger_name=__name__)


class RedisRepository(RedisRepositoryProtocol):
    """
    Implementation of RedisRepositoryProtocol
    """

    def __init__(self, redis: Redis, namespace: str):
        self.redis = redis
        self.namespace = namespace

    def _get_key(self, key: str) -> str:
        return f"{self.namespace}:{key}"

    async def create(self, obj_in: dict[str, Any]) -> None:
        key = self._get_key(obj_in["key"])
        try:
            await self.redis.setex(key, obj_in["expires_in"], obj_in["value"])
        except RedisError as e:
            msg = f"Failed to create key {key}: {e}"
            logger.error(msg=msg)
            raise RedisCreateError(msg)

    async def get(self, key: str) -> str | None:
        key = self._get_key(key)
        try:
            return await self.redis.get(key)
        except RedisError as e:
            msg = f"Failed to get key {key}: {e}"
            logger.error(msg=msg)
            raise RedisGetError(msg)

    async def update(self, obj_id: str, obj_in: dict[str, Any]) -> None:
        key = self._get_key(obj_id)
        try:
            await self.redis.setex(key, obj_in["expires_in"], obj_in["value"])
        except RedisError as e:
            msg = f"Failed to update key {key}: {e}"
            logger.error(msg=msg)
            raise RedisUpdateError(msg)

    async def delete(self, key: str) -> None:
        key = self._get_key(key)
        try:
            await self.redis.delete(key)
        except RedisError as e:
            msg = f"Failed to delete key {key}: {e}"
            logger.error(msg=msg)
            raise RedisDeleteError(msg)

    async def list(self, key: str | None = None) -> list[str]:
        try:
            keys = await self.redis.keys(f"{self.namespace}:*")
            return [await self.redis.get(key) for key in keys]
        except RedisError as e:
            msg = f"Failed to list keys: {e}"
            logger.error(msg=msg)
            raise RedisListError(msg)
