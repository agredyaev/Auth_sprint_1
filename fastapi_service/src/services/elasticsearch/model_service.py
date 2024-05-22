from typing import Any

from elasticsearch import NotFoundError

from fastapi_service.src.core.exceptions import BadRequestError
from fastapi_service.src.core.logger import setup_logging
from fastapi_service.src.services.elasticsearch.client import ElasticsearchClientInterface
from fastapi_service.src.services.redis.cache import ModelCacheDecorator

logger = setup_logging(logger_name=__name__)


class ModelService:
    """
    Contains business logic for working with Elasticsearch models.
    """

    def __init__(self, client: ElasticsearchClientInterface):
        self.client = client

    @ModelCacheDecorator(key="model_id")
    async def get_model_by_id(self, *, index: str, model_id: str) -> dict[str, Any] | None:
        return await self._fetch_model(index=index, model_id=model_id)

    async def _fetch_model(self, index: str, model_id: str) -> dict[str, Any] | None:
        try:
            document = await self.client.get(index=index, id_=model_id)
            return document["_source"]

        except NotFoundError:
            logger.info(msg="Model with ID {model_id} not found in index {index}.")
            return None

        except BadRequestError:
            logger.exception(msg="Failed to fetch model with ID {model_id} from index {index}.")
            return None

        except Exception:
            logger.exception(msg=f"Failed to fetch model with ID {model_id} from index {index}.")
            return None
