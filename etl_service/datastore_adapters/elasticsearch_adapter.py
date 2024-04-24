from .base_adapter import DatastoreAdapter
from ..utility.logger import setup_logging
from elasticsearch import Elasticsearch, helpers
import elastic_transport
from ..utility.backoff import backoff, datastore_reconnect
from ..utility.exceptions import ElasticsearchConnectionError
from ..utility.support_functions import split_into_chunks

from pydantic import AnyHttpUrl

logger = setup_logging()


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
        self._connection = self.Elasticsearch(self._dsn, *self.args, **self.kwargs)

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
    def chunked_bulk(self, actions: list, batch_size: int, *args, **kwargs) -> None:
        """ Process actions in chunks and send them to Elasticsearch in bulk. """

        for action_chunk in split_into_chunks(actions, batch_size):
            try:
                helpers.bulk(self._connection, actions=action_chunk, *args, **kwargs)
            except Exception as e:
                logger.error(f"Error during bulk operation: {e}")
