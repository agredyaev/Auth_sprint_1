from functools import lru_cache
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from auth_service.src.db.postgres import get_session
from auth_service.src.services.user_repository.service import UserRepository, UserRepositoryProtocol


@lru_cache()
def get_user_repository(db: AsyncSession = Depends(get_session)) -> UserRepositoryProtocol:
    """
    Provider for user repository
    """
    return UserRepository(db)
