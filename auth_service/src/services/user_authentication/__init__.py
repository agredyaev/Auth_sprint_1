# from functools import lru_cache
# from fastapi import Depends
#
# from auth_service.src.services.repositories.user import get_user_repository, UserRepositoryProtocol
# from auth_service.src.services.user_authentication.service import UserAuthenticationService, UserAuthenticationProtocol
#
#
# @lru_cache()
# def get_user_authentication_service(
#     user_repo: UserRepositoryProtocol = Depends(get_user_repository)
# ) -> UserAuthenticationProtocol:
#     """
#     Provider for UserAuthenticationService
#     """
#     return UserAuthenticationService(user_repo)
