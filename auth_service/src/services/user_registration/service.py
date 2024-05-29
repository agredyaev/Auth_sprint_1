from typing import Protocol
from src.schemas.auth import UserCreate, TokenData
from src.repositories.user_repository import UserRepositoryProtocol
from src.repositories.token_repository import TokenRepositoryProtocol

class UserRegistrationProtocol(Protocol):
    async def register_user(self, user: UserCreate) -> TokenData:
        ...

class UserRegistrationService(UserRegistrationProtocol):
    def __init__(self, user_repo: UserRepositoryProtocol, token_repo: TokenRepositoryProtocol):
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def register_user(self, user: UserCreate) -> TokenData:
        new_user = await self.user_repo.create_user(user)
        # Логика генерации токена
        token_data = TokenData(access_token="access", refresh_token="refresh", expires_in=3600)
        await self.token_repo.save_token(str(new_user.id), token_data)
        return token_data
