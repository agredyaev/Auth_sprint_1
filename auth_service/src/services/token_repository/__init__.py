from functools import lru_cache
from fastapi import Depends

from auth_service.src.db.redis import get_redis

from auth_service.src.services.token_repository.service import TokenRepository, TokenRepositoryProtocol


@lru_cache()
def get_token_repository(redis=Depends(get_redis)) -> TokenRepositoryProtocol:
    """
    Provider for TokenRepository
    """
    return TokenRepository(redis)
