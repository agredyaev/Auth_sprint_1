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
from auth_service.src.interfaces.repositories import CreateSchemaType, RedisRepositoryProtocol, UpdateSchemaType

logger = setup_logging(logger_name=__name__)


class RedisRepository(RedisRepositoryProtocol):
    """
    Implementation of RedisRepositoryProtocol
    """

    def __init__(self, redis: Redis):
        self.redis = redis

    async def create(self, obj_in: CreateSchemaType) -> None:
        try:
            await self.redis.setex(**obj_in.model_dump())
        except RedisError as e:
            msg = f"Failed to create {obj_in}: {e}"
            logger.error(msg=msg)
            raise RedisCreateError(msg)

    async def get(self, key: str) -> str | None:
        try:
            return await self.redis.get(key)
        except RedisError as e:
            msg = f"Failed to get key {key}: {e}"
            logger.error(msg=msg)
            raise RedisGetError(msg)

    async def update(self, obj_id: str, obj_in: UpdateSchemaType) -> None:
        try:
            await self.redis.setex(**obj_in.model_dump())
        except RedisError as e:
            msg = f"Failed to update {obj_in}: {e}"
            logger.error(msg=msg)
            raise RedisUpdateError(msg)

    async def delete(self, key: str) -> None:
        try:
            await self.redis.delete(key)
        except RedisError as e:
            msg = f"Failed to delete key {key}: {e}"
            logger.error(msg=msg)
            raise RedisDeleteError(msg)

    async def list(self, key: str | None = None) -> list[str]:
        try:
            keys = await self.redis.keys("*")
            return [await self.redis.get(key) for key in keys]
        except RedisError as e:
            msg = f"Failed to list keys: {e}"
            logger.error(msg=msg)
            raise RedisListError(msg)
