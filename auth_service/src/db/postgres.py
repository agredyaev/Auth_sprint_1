from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from auth_service.src.core.logger import setup_logging

logger = setup_logging(logger_name=__name__)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a session for database operations"""
    from auth_service.src.core.config import settings

    async_engine = create_async_engine(url=settings.pg.dsn, echo=settings.pg.echo_sql_queries, future=True)
    async_session = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)

    async with async_session() as session:
        async with session.begin():
            try:
                yield session
            except SQLAlchemyError as e:
                await session.rollback()
                logger.exception(msg="Database error", exc_info=e)
                raise e
