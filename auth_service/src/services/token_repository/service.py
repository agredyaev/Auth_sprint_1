from typing import Protocol
from redis.asyncio import Redis
from auth_service.src.schemas.auth import TokenData


class TokenRepositoryProtocol(Protocol):
    async def store(self, user_id: str, token: TokenData) -> None:
        ...

    async def get(self, user_id: str) -> TokenData | None:
        ...

    async def delete(self, user_id: str) -> None:
        ...


class TokenRepository:
    """
    Implementation of TokenRepositoryProtocol
    """
    def __init__(self, redis: Redis):
        self.redis = redis

    async def store(self, user_id: str, token: TokenData) -> None:
        await self.redis.set(user_id, token.json(), ex=token.expires_in)

    async def get(self, user_id: str) -> TokenData | None:
        token_data = await self.redis.get(user_id)
        if token_data:
            return TokenData.parse_raw(token_data)
        return None

    async def delete(self, user_id: str) -> None:
        await self.redis.delete(user_id)
