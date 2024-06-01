# from functools import lru_cache
# from fastapi import Depends
#
# from auth_service.src.services.repositories.user import get_user_repository, UserRepositoryProtocol
# from auth_service.src.services.repositories.token import get_token_repository, TokenRepositoryProtocol
# from auth_service.src.services.user_registration.service import UserRegistrationService, UserRegistrationProtocol
#
#
# @lru_cache()
# def get_user_registration_service(
#     user_repo: UserRepositoryProtocol = Depends(get_user_repository),
#     token_repo: TokenRepositoryProtocol = Depends(get_token_repository)
# ) -> UserRegistrationProtocol:
#     """
#     Provider for UserRegistrationService
#     """
#     return UserRegistrationService(user_repo, token_repo)
