from typing import Any, Protocol, Sequence, TypeVar

T = TypeVar("T", covariant=True)
CreateSchemaType = TypeVar("CreateSchemaType", bound=Any, contravariant=True)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=Any, contravariant=True)
MergeSchemaType = TypeVar("MergeSchemaType", bound=Any, contravariant=True)
AttrType = TypeVar("AttrType", bound=Any, contravariant=True)


class RepositoryProtocol(Protocol[T, CreateSchemaType, UpdateSchemaType, AttrType]):
    """
    Base repository interface
    """

    async def create(self, obj_in: CreateSchemaType) -> T:
        """
        Creates a new object
        """
        ...

    async def get(self, obj_id: AttrType) -> T | None:
        """
        Gets object by id
        """
        raise NotImplementedError

    async def update(self, obj_id: AttrType, obj_in: UpdateSchemaType) -> None:
        """
        Updates object
        """
        raise NotImplementedError

    async def delete(self, obj_id: AttrType) -> None:
        """
        Deletes object
        """
        raise NotImplementedError

    async def list(self, obj_id: AttrType | None = None) -> Sequence[T]:
        """
        Gets a sequence of objects
        """
        raise NotImplementedError


class MergeRepositoryProtocol(Protocol[MergeSchemaType]):
    async def merge(self, obj_in: MergeSchemaType) -> T:
        """
        Merge object
        """
        raise NotImplementedError
