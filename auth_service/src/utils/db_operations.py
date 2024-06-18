from typing import Any, Sequence, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=Any)


async def commit_to_db(session: AsyncSession, db_obj: T, merge: bool = False) -> T:
    """
    Commit object to database
    :param session:
    :param db_obj:
    :param merge:
    :return:
    """
    if merge:
        db_obj = await session.merge(db_obj)
    else:
        session.add(db_obj)
    await session.flush()
    return db_obj


async def delete_from_db(session: AsyncSession, db_obj: Any) -> None:
    """
    Delete object from database
    :param session:
    :param db_obj:
    :return:
    """
    await session.delete(db_obj)


async def execute_single_query(session: AsyncSession, query: Any) -> T | None:
    """
    Execute query and return a single result
    :param session: SQLAlchemy async session
    :param query: SQLAlchemy query (Select, Delete, Insert)
    :return: single result or none
    """
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def execute_list_query(session: AsyncSession, query: Any) -> Sequence[T]:
    """
    Execute query and return a list of results
    :param session: SQLAlchemy async session
    :param query: SQLAlchemy query (Select, Delete, Insert)
    :return: List of results for Select query, empty list for Delete and Insert queries
    """
    result = await session.execute(query)
    return result.scalars().all()


def update_object(db_obj: Any, obj_in: Any) -> None:
    """
    Update object
    :param db_obj:
    :param obj_in:
    :return:
    """
    for key, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
