import elastic_transport
from elasticsearch import Elasticsearch, helpers
from pydantic import AnyHttpUrl

from etl_service.datastore_adapters.base_adapter import DatastoreAdapter
from etl_service.utility.backoff import backoff, datastore_reconnect
from etl_service.utility.exceptions import ElasticsearchConnectionError
from etl_service.utility.logger import setup_logging
from etl_service.utility.support_functions import split_into_chunks

logger = setup_logging(logger_name=__name__)


class ElasticsearchAdapter(DatastoreAdapter):
    """Elasticsearch adapter class."""

    base_adapter_exceptions = elastic_transport.ConnectionError
    _connection: Elasticsearch

    def __init__(self, dsn: AnyHttpUrl, *args, **kwargs):
        super().__init__(dsn, *args, **kwargs)

    @property
    def is_connected(self) -> bool:
        """Check if client is connected."""
        return self._connection.ping()

    @backoff(retry_exceptions=(base_adapter_exceptions, ElasticsearchConnectionError))
    def connect(self) -> None:
        """Connect to client."""

        self._connection = Elasticsearch(self._dsn.unicode_string(), *self.args, **self.kwargs)

        if not self.is_connected:
            raise ElasticsearchConnectionError(f"Unable to connect to the client {self.__repr__()}")

        logger.info("Connected to client: %r", self)

    def reconnect(self) -> None:
        super().reconnect()

    @backoff(retry_exceptions=base_adapter_exceptions)
    def close(self) -> None:
        super().close()

    @backoff(retry_exceptions=(base_adapter_exceptions, elastic_transport.SerializationError))
    @datastore_reconnect
    def index_exists(self, index: str) -> None:
        return self._connection.indices.exists(index=index)

    @backoff(retry_exceptions=(base_adapter_exceptions, elastic_transport.SerializationError))
    @datastore_reconnect
    def index_create(self, index: str, body: dict) -> None:
        return self._connection.indices.create(index=index, body=body)

    @backoff(retry_exceptions=(base_adapter_exceptions, elastic_transport.SerializationError))
    @datastore_reconnect
    def bulk(self, *args, **kwargs) -> None:
        helpers.bulk(self._connection, *args, **kwargs)

    @backoff(retry_exceptions=(base_adapter_exceptions, elastic_transport.SerializationError))
    @datastore_reconnect
    def chunked_bulk(self, items: list, batch_size: int, *args, **kwargs) -> None:
        """Process actions in chunks and send them to Elasticsearch in bulk."""
        raise_on_exception = kwargs.get("raise_on_exception", False)
        for action_chunk in split_into_chunks(items, batch_size):
            try:
                helpers.bulk(self._connection, actions=action_chunk, *args, **kwargs)
            except Exception as e:
                logger.error(f"Error during bulk operation: {e}")
                if raise_on_exception:
                    raise
