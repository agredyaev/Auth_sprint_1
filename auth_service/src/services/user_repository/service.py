from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from auth_service.src.models.user import User
from auth_service.src.schemas.user import UserCreate


class UserRepositoryProtocol(Protocol):
    async def create_user(self, user: UserCreate) -> User:
        ...

    async def get_user_by_login(self, login: str) -> User | None:
        ...

    async def update_user(self, user: User) -> User:
        ...


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: UserCreate) -> User:
        new_user = User(**user.dict())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def get_user_by_login(self, login: str) -> User | None:
        result = await self.session.execute(select(User).where(User.login == login))
        return result.scalars().first()

    async def update_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
