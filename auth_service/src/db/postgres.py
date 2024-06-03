from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from auth_service.src.core.config import settings

Base = declarative_base()

async_engine = create_async_engine(url=settings.pg.dsn, echo=settings.pg.echo_sql_queries, future=True)
async_session = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


async def create_database() -> None:
    """Create database if it doesn't exist"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def purge_database() -> None:
    """Drop all tables in the database"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a session for database operations"""
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
