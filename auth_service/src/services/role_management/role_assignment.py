# from typing import Protocol
# from uuid import UUID
# from sqlalchemy.ext.asyncio import AsyncSession
# from auth_service.src.models.role import UserRole
# from auth_service.src.utils.db_operations import add_and_commit, refresh_instance, execute_query, delete_and_commit
#
#
# class RoleAssignmentProtocol(Protocol):
#     async def assign_role_to_user(self, user_id: UUID, role_id: UUID) -> UserRole:
#         ...
#
#     async def remove_role_from_user(self, user_id: UUID, role_id: UUID) -> None:
#         ...
#
#     async def check_user_role(self, user_id: UUID, role_name: str) -> bool:
#         ...
#
#
# class RoleAssignmentService:
#     """
#     Implementation of RoleAssignmentProtocol
#     """
#     def __init__(self, db: AsyncSession):
#         self.db = db
#
#     async def assign_role_to_user(self, user_id: UUID, role_id: UUID) -> UserRole:
#         new_user_role = UserRole(user_id=user_id, role_id=role_id)
#         await add_and_commit(self.db, new_user_role)
#         await refresh_instance(self.db, new_user_role)
#         return new_user_role
#
#     async def remove_role_from_user(self, user_id: UUID, role_id: UUID) -> None:
#         result = await execute_query(
#             self.db,
#             select(UserRole).where(UserRole.user_id == user_id, UserRole.role_id == role_id)
#         )
#         user_role = result.scalars().first()
#         if user_role:
#             await delete_and_commit(self.db, user_role)
#
#     async def check_user_role(self, user_id: UUID, role_name: str) -> bool:
#         result = await execute_query(
#             self.db,
#             select(UserRole)
#             .join(Role)
#             .where(UserRole.user_id == user_id, Role.name == role_name)
#         )
#         return result.scalars().first() is not None
