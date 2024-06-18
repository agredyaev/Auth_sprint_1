from redis.asyncio import Redis

from auth_service.src.interfaces.repositories import TokenRepositoryProtocol
from auth_service.src.repositories.redis_db import RedisRepository
from auth_service.src.schemas.request import Token


class TokenRepository(TokenRepositoryProtocol[Token], RedisRepository):
    """Implementation of TokenRepositoryProtocol"""

    def __init__(self, redis: Redis):
        super().__init__(redis)

    async def set_token(self, obj_in: Token) -> None:
        await self.create(obj_in)

    async def get_token(self, obj_in: Token) -> str | None:
        return await self.get(obj_in.name)
