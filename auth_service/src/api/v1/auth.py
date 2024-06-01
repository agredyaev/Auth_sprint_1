# from fastapi import APIRouter, Depends
# from async_fastapi_jwt_auth import AuthJWT
# from auth_service.src.services import (
#     get_user_registration_service,
#     get_user_authentication_service,
#     get_token_management_service
# )
# from auth_service.src.schemas.auth import UserCreate, TokenData
#
# auth_router = APIRouter()
#
#
# @auth_router.post("/signup", response_model=TokenData)
# async def register_user(user: UserCreate):
#     user_registration_service = get_user_registration_service()
#     return await user_registration_service.register_user(user)
#
#
# @auth_router.post("/login", response_model=TokenData)
# async def login_user(username: str, password: str, Authorize: AuthJWT = Depends()):
#     user_authentication_service = get_user_authentication_service()
#     return await user_authentication_service.authenticate_user(username, password, Authorize)
#
#
# @auth_router.post("/refresh", response_model=TokenData)
# async def refresh_token(Authorize: AuthJWT = Depends()):
#     token_management_service = get_token_management_service()
#     return await token_management_service.refresh_token(Authorize)
#
#
# @auth_router.post("/logout")
# async def logout_user(token: str, Authorize: AuthJWT = Depends()):
#     user_authentication_service = get_user_authentication_service()
#     await user_authentication_service.logout_user(token, Authorize)
#     return {"message": "Successfully logged out"}
