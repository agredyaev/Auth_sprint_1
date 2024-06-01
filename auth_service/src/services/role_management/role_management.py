# from auth_service.src.services.role_management.role_assignment import RoleAssignmentProtocol, RoleAssignmentService
# from auth_service.src.services.role_management.role_creation import RoleCreationProtocol, RoleCreationService
# from auth_service.src.services.role_management.role_modification import RoleModificationProtocol, \
#     RoleModificationService
# from auth_service.src.services.role_management.role_retrival import RoleRetrievalProtocol, RoleRetrievalService
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from typing import Protocol
#
#
# class RoleManagementProtocol(Protocol):
#
#     @property
#     def role_creation_service(self) -> RoleCreationProtocol:
#         ...
#
#     @property
#     def role_retrieval_service(self) -> RoleRetrievalProtocol:
#         ...
#
#     @property
#     def role_modification_service(self) -> RoleModificationProtocol:
#         ...
#
#     @property
#     def role_assignment_service(self) -> RoleAssignmentProtocol:
#         ...
#
#
# class RoleManagementService:
#     """
#     Implementation of RoleManagementProtocol
#     """
#
#     def __init__(self, db: AsyncSession):
#         self.db = db
#
#     @property
#     def role_creation_service(self) -> RoleCreationProtocol:
#         return RoleCreationService(db=self.db)
#
#     @property
#     def role_retrieval_service(self) -> RoleRetrievalProtocol:
#         return RoleRetrievalService(db=self.db)
#
#     @property
#     def role_modification_service(self) -> RoleModificationProtocol:
#         return RoleModificationService(db=self.db)
#
#     @property
#     def role_assignment_service(self) -> RoleAssignmentProtocol:
#         return RoleAssignmentService(db=self.db)
