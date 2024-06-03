from typing import Any, Sequence, Type, TypeVar, Union

from sqlalchemy import Select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.src.core.logger import setup_logging

logger = setup_logging(logger_name=__name__)

T = TypeVar("T", bound=Any)


async def commit_to_db(session: AsyncSession, db_obj: Any, merge: bool = False) -> None:
    """
    Commit object to database
    :param session:
    :param db_obj:
    :param merge:
    :return:
    """
    async with session.begin():
        try:
            if merge:
                await session.merge(db_obj)
            else:
                session.add(db_obj)
            await session.commit()
        except SQLAlchemyError as e:
            logger.exception("Database operation failed:", exc_info=e)
            await session.rollback()
            raise e


async def delete_from_db(session: AsyncSession, db_obj: Any) -> None:
    """
    Delete object from database
    :param session:
    :param db_obj:
    :return:
    """
    async with session.begin():
        try:
            await session.delete(db_obj)
            await session.commit()
        except SQLAlchemyError as e:
            logger.exception("Failed to delete object:", exc_info=e)
            await session.rollback()
            raise e


async def execute_single_query(session: AsyncSession, query: Select) -> Union[T, None]:
    """
    Execute query and return a single result
    :param session:
    :param query:
    :return:
    """
    try:
        result = await session.execute(query)
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        logger.exception("Failed to execute query:", exc_info=e)
        raise e


async def execute_list_query(session: AsyncSession, query: Select) -> Sequence[T]:
    """
    Execute query and return a list of results
    :param session:
    :param query:
    :return:
    """
    try:
        result = await session.execute(query)
        return result.scalars().all()
    except SQLAlchemyError as e:
        logger.exception("Failed to execute query:", exc_info=e)
        raise e


def update_object(db_obj: Any, obj_in: Any) -> None:
    """
    Update object
    :param db_obj:
    :param obj_in:
    :return:
    """
    for key, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)


def to_pydantic(db_obj: T, pydantic_model: Type[Any]) -> Any | None:
    try:
        return pydantic_model(**db_obj.__dict__)
    except (TypeError, AttributeError) as e:
        logger.exception("Failed to convert object to Pydantic model:", exc_info=e)
        return None
