from async_fastapi_jwt_auth import AuthJWT
from fastapi import HTTPException
from typing import Protocol
from auth_service.src.schemas.auth import TokenData


class TokenManagementProtocol(Protocol):
    async def refresh(self, Authorize: AuthJWT) -> TokenData:
        ...


class TokenManagementService:
    async def refresh(self, Authorize: AuthJWT) -> TokenData:
        try:
            Authorize.jwt_refresh_token_required()
            user_id = Authorize.get_jwt_subject()
            access_token = Authorize.create_access_token(subject=user_id)
            refresh_token = Authorize.create_refresh_token(subject=user_id)
            return TokenData(access_token=access_token, refresh_token=refresh_token)
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))
