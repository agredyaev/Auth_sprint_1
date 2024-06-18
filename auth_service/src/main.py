import uvicorn
from async_fastapi_jwt_auth import AuthJWT  # type: ignore
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from auth_service.src.api import router as api_router
from auth_service.src.core import config, exceptions, logger
from auth_service.src.utils import lifespan
from auth_service.src.utils.permission_middleware import PermissionMiddleware

log_config = logger.get_log_config()


@AuthJWT.load_config
def get_config() -> config.JWTSettings:
    return config.settings.jwt


app = FastAPI(
    lifespan=lifespan.get_lifespan,
    default_response_class=ORJSONResponse,
    title=config.settings.general.project_name,
    version=config.settings.general.version,
    docs_url=config.settings.general.docs_url,
    openapi_url=config.settings.general.openapi_url,
)

app.add_middleware(PermissionMiddleware)
app.include_router(api_router, prefix=config.settings.api.prefix)
exceptions.register_exception_handlers(app=app)


if __name__ == "__main__":
    uvicorn.run(
        app=config.settings.uvicorn.app,
        host=config.settings.uvicorn.host,
        port=config.settings.uvicorn.port,
        reload=True,
        log_config=log_config,
    )
