# from functools import lru_cache
# from fastapi import Depends
#
# from auth_service.src.services.repositories.token import TokenRepositoryProtocol, get_token_repository
#
# from auth_service.src.services.token_management.service import TokenManagementService, TokenManagementProtocol
#
#
# @lru_cache()
# def get_token_management_service(
#     token_repo: TokenRepositoryProtocol = Depends(get_token_repository)
# ) -> TokenManagementProtocol:
#     """
#     Provider for TokenManagementService
#     """
#     return TokenManagementService(token_repo=token_repo)
