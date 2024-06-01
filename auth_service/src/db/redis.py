from redis.asyncio import Redis

from auth_service.src.core.config import settings
from auth_service.src.core.exceptions import RedisConnectionError
from auth_service.src.core.logger import setup_logging

logger = setup_logging(logger_name=__name__)

redis: Redis | None = None


async def redis_open() -> None:
    """
    Open Redis connection
    """
    global redis
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        username=settings.redis.user.get_secret_value(),
        password=settings.redis.password.get_secret_value(),
        db=settings.redis.db_number,
    )


async def get_redis() -> Redis:
    """
    Get Redis instance
    :return Redis instance
    """
    if redis is None:
        logger.critical("Redis is not initialized")
        raise RedisConnectionError("Redis client has not been initialized.")
    return redis
