import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from fastapi_service.src.api import router as api_router
from fastapi_service.src.core import config, logger, utils

log_config = logger.get_log_config()


app = FastAPI(
    lifespan=utils.lifespan,
    default_response_class=ORJSONResponse,
    title=config.settings.general.project_name,
    version=config.settings.general.version,
    docs_url=config.settings.general.docs_url,
    openapi_url=config.settings.general.openapi_url,
)

app.include_router(api_router, prefix=config.settings.api.prefix)

if __name__ == "__main__":
    uvicorn.run(
        app=config.settings.uvicorn.app,
        host=config.settings.uvicorn.host,
        port=config.settings.uvicorn.port,
        reload=True,
        log_config=log_config,
    )
