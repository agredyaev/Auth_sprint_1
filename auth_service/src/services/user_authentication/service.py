# from async_fastapi_jwt_auth import AuthJWT
# from fastapi import HTTPException
# from typing import Protocol
# # from auth_service.src.schemas.auth import TokenData
# # from auth_service.src.services.repositories.user import UserRepositoryProtocol
#
#
# class UserAuthenticationProtocol(Protocol):
#     async def authenticate(self, username: str, password: str, Authorize: AuthJWT) -> TokenData:
#         ...
#
#     async def logout(self, user_id: str, Authorize: AuthJWT) -> None:
#         ...
#
#
# class UserAuthenticationService:
#     """
#     Implementation of UserAuthenticationProtocol
#     """
#
#     def __init__(self, user_repo: UserRepositoryProtocol):
#         self.user_repo = user_repo
#
#     async def authenticate(self, username: str, password: str, Authorize: AuthJWT) -> TokenData:
#         user = await self.user_repo.get_user_by_login(username)
#         if user and user.check_password(password):
#             access_token = Authorize.create_access_token(subject=str(user.id))
#             refresh_token = Authorize.create_refresh_token(subject=str(user.id))
#             return TokenData(access_token=access_token, refresh_token=refresh_token)
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#
#     async def logout(self, user_id: str, Authorize: AuthJWT) -> None:
#         await Authorize.jwt_required()
#         Authorize.unset_jwt_cookies()
