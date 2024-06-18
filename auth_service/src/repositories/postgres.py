from typing import Any, Sequence, Type, TypeVar
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth_service.src.core.logger import setup_logging
from auth_service.src.interfaces.repositories import (
    CreateSchemaType,
    MergeSchemaType,
    PostgresRepositoryProtocol,
    UpdateSchemaType,
)
from auth_service.src.utils.db_operations import (
    commit_to_db,
    delete_from_db,
    execute_list_query,
    execute_single_query,
    update_object,
)

logger = setup_logging(logger_name=__name__)

T = TypeVar("T", bound=Any)


class PostgresRepository(PostgresRepositoryProtocol[T]):
    """
    Implementation of PostgresRepositoryProtocol.
    """

    _model: Type[T]

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session: AsyncSession = db_session

    async def create(self, obj_in: CreateSchemaType) -> T:
        db_obj = self._model(**obj_in.model_dump())
        await commit_to_db(self.db_session, db_obj)
        return db_obj

    async def get(self, obj_id: UUID) -> T | None:
        query = select(self._model).filter(self._model.id == obj_id)
        db_obj: T | None = await execute_single_query(self.db_session, query)
        return db_obj

    async def update(self, obj_id: UUID, obj_in: UpdateSchemaType) -> None:
        db_obj = await self.get(obj_id)
        if db_obj:
            update_object(db_obj, obj_in)
            await commit_to_db(self.db_session, db_obj)
        else:
            logger.error(f"Object with ID {obj_id} not found.")

    async def delete(self, obj_id: UUID) -> None:
        db_obj = await self.get(obj_id)
        if db_obj:
            await delete_from_db(self.db_session, db_obj)
        else:
            logger.error(f"Object with ID {obj_id} not found.")

    async def list(self, obj_id: UUID | None = None) -> Sequence[T]:
        query = select(self._model)
        if obj_id:
            query = query.filter(self._model.id == obj_id)
        return await execute_list_query(self.db_session, query)

    async def merge(self, obj_in: MergeSchemaType) -> T:
        db_obj = self._model(**obj_in.model_dump())
        await commit_to_db(self.db_session, db_obj, merge=True)
        return db_obj
