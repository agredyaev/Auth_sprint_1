import redis.exceptions
from etl_service.datastore_adapters.base_adapter import DatastoreAdapter
from pydantic import RedisDsn
from redis.client import Redis
from redis.typing import EncodableT, KeyT

from etl_service.utility.backoff import backoff, datastore_reconnect
from etl_service.utility.exceptions import RedisConnectionError
from etl_service.utility.logger import setup_logging

logger = setup_logging()


class RedisAdapter(DatastoreAdapter):
    """Redis adapter class."""

    base_adapter_exceptions = redis.exceptions.RedisError
    _connection: Redis

    def __init__(self, dsn: RedisDsn, *args, **kwargs):
        super().__init__(dsn, *args, **kwargs)

    @property
    def is_connected(self) -> bool:
        """Check if the connection is alive."""
        try:
            return self._connection is not None and self._connection.ping()
        except redis.exceptions.ConnectionError:
            return False

    @backoff(retry_exceptions=(base_adapter_exceptions, RedisConnectionError))
    def connect(self) -> None:
        """Connect to client."""
        self._connection = Redis(
            host=self._dsn.host,
            port=self._dsn.port,
            username=self._dsn.username,
            password=self._dsn.password,
            db=self._dsn.path[1:],
            *self.args,
            **self.kwargs,
        )

        if not self.is_connected:
            raise RedisConnectionError(
                f"Unable to connect to the client {self.__repr__()}"
            )

        logger.info("Connected to client: %r", self)

    def reconnect(self) -> None:
        super().reconnect()

    @backoff(retry_exceptions=base_adapter_exceptions)
    def close(self) -> None:
        super().close()

    @backoff(retry_exceptions=base_adapter_exceptions)
    @datastore_reconnect
    def keys(self, pattern, **kwargs) -> list[str]:
        return self._connection.keys(pattern, **kwargs)

    @backoff(retry_exceptions=base_adapter_exceptions)
    @datastore_reconnect
    def exists(self, *names: KeyT) -> int:
        return self._connection.exists(*names)

    @backoff(retry_exceptions=base_adapter_exceptions)
    @datastore_reconnect
    def get(self, name: KeyT) -> bytes | None:
        return self._connection.get(name)

    @backoff(retry_exceptions=base_adapter_exceptions)
    @datastore_reconnect
    def set(self, name: KeyT, value: EncodableT, *args, **kwargs) -> None:
        return self._connection.set(name, value, *args, **kwargs)
