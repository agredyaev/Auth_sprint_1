from abc import ABC, abstractmethod
from typing import Any, Tuple, Type, Union

from pydantic import AnyUrl

from etl_service.utility.logger import setup_logging

logger = setup_logging(logger_name=__name__)


class BaseAdapter(ABC):
    """Base class for data adapters."""

    base_adapter_exceptions: Union[Tuple[Type[Exception]], Type[Exception]]

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """Check if client is connected."""
        raise NotImplementedError

    @abstractmethod
    def reconnect(self) -> None:
        """Reconnect to client."""
        raise NotImplementedError

    @abstractmethod
    def connect(self) -> None:
        """Connect to client."""
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        """Close connection to client."""
        raise NotImplementedError


class DatastoreAdapter(BaseAdapter, ABC):
    """Datastore adapter class."""

    base_adapter_exceptions: Union[Tuple[Type[Exception]], Type[Exception]]
    _connection: Any

    def __init__(self, dsn: AnyUrl, *args, **kwargs):
        self._dsn = dsn
        self.args = args
        self.kwargs = kwargs
        self.connect()

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """Check if client is connected."""
        raise NotImplementedError

    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError

    def reconnect(self) -> None:
        """Reconnect to client."""
        if not self.is_connected:
            logger.info(
                "Lost connection to client: %r. Attempting to establish new connection...",
                self,
            )
            self.connect()

    def close(self) -> None:
        """Close connection to client."""
        if self.is_connected:
            logger.info("Closing connection to client: %r", self)
            self._connection.close()

        self._connection = None

    def __repr__(self):
        return f"{self.__class__.__name__}({self._dsn})"
