from typing import Any

from async_fastapi_jwt_auth import AuthJWT  # type: ignore


@AuthJWT.token_in_denylist_loader
async def check_if_token_in_denylist(decrypted_token: Any) -> bool:
    """Check if token in denylist"""

    from auth_service.src.db import get_redis
    from auth_service.src.repositories import get_token_repository
    from auth_service.src.schemas.request import TokenGet

    jti = decrypted_token.get("jti")
    redis = await get_redis()
    token_repo = get_token_repository(redis=redis)
    entry = await token_repo.get_token(obj_in=TokenGet(name=jti))
    if not entry:
        return False
    return entry == "true"
