# from typing import Protocol
#
# from sqlalchemy.ext.asyncio import AsyncSession
# from auth_service.src.models.role import Role
# from auth_service.src.schemas.role import RoleCreate
# from auth_service.src.utils.db_operations import add_and_commit, refresh_instance
#
#
# class RoleCreationProtocol(Protocol):
#     async def create_role(self, role: RoleCreate) -> Role:
#         ...
#
#
# class RoleCreationService:
#     """
#     Implementation of RoleCreationProtocol
#     """
#     def __init__(self, db: AsyncSession):
#         self.db = db
#
#     async def create_role(self, role: RoleCreate) -> Role:
#         new_role = Role(**role.dict())
#         await add_and_commit(self.db, new_role)
#         await refresh_instance(self.db, new_role)
#         return new_role
