from typing import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture(scope="module")
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

    from tests.auth_service.settings import config

    engine = create_async_engine(config.infra.pg.dsn, future=True)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session
        await session.close()


@pytest_asyncio.fixture(scope="module", autouse=True)
async def clear_login_history(async_session: AsyncSession) -> None:
    query = text("""
        DELETE FROM auth.login_history 
        WHERE 1=1;
    """)
    await async_session.execute(query)
    await async_session.commit()


@pytest_asyncio.fixture(scope="module", autouse=True)
async def clear_users(async_session: AsyncSession) -> None:
    query = text("""
        DELETE FROM auth.user 
        WHERE email NOT IN (
            'admin@example.com'
        );
    """)
    await async_session.execute(query)
    await async_session.commit()


@pytest_asyncio.fixture(scope="module", autouse=True)
async def clear_roles(async_session: AsyncSession) -> None:
    query = text("""
    DELETE FROM auth.role 
        WHERE id NOT IN (
            '37a8eec1-ce19-687d-132f-e29051dca629',
            '8c6976e5-b541-0415-bde9-08bd4dee15df'
        );
    """)
    await async_session.execute(query)
    await async_session.commit()
