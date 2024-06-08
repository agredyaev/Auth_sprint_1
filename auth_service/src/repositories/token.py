from redis.asyncio import Redis

from auth_service.src.interfaces.repositories import TokenRepositoryProtocol
from auth_service.src.repositories.redis_db import RedisRepository
from auth_service.src.schemas.request import Token


class TokenRepository(TokenRepositoryProtocol, RedisRepository):
    """Implementation of TokenRepositoryProtocol"""
    def __init__(self, redis: Redis):
        super().__init__(redis)

    async def set_token(self, obj_in: Token) -> None:
        await self.create(obj_in)

    async def get_token(self, obj_in: Token) -> None:
        await self.get(obj_in.name)

    async def is_in_denylist_or_not_exist(self, obj_in: Token) -> bool:
        stored_token = await self.get(obj_in.name)
        return stored_token == "true" or not stored_token
