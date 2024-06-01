# from functools import lru_cache
# from fastapi import Depends
# from sqlalchemy.ext.asyncio import AsyncSession
# from auth_service.src.db.postgres import get_session
# from auth_service.src.services.role_management.role_management import RoleManagementService, \
#     RoleManagementProtocol
#
#
# @lru_cache()
# def get_role_management_service(
#     db: AsyncSession = Depends(get_session)
# ) -> RoleManagementProtocol:
#     """
#     Provider for RoleManagementProvider
#     """
#     return RoleManagementService(db)
