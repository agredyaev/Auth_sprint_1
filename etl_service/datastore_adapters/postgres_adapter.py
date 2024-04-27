import contextlib
from typing import Any

import psycopg2
from psycopg2.extensions import connection as pg_conn
from psycopg2.extensions import cursor as pg_cursor
from psycopg2.extras import DictCursor
from psycopg2.sql import SQL
from pydantic import PostgresDsn

from etl_service.datastore_adapters.base_adapter import BaseAdapter, DatastoreAdapter
from etl_service.utility.backoff import backoff, datastore_reconnect
from etl_service.utility.logger import setup_logging

logger = setup_logging()


class PostgresAdapter(DatastoreAdapter):
    """Postgres adapter class for managing database connections."""

    base_adapter_exceptions = psycopg2.OperationalError
    _connection: pg_conn = None

    def __init__(self, dsn: PostgresDsn, *args, **kwargs):
        super().__init__(dsn, *args, **kwargs)

    @property
    def is_connected(self) -> bool:
        """Checks if the database connection is open."""
        return self._connection and not self._connection.closed

    @backoff(retry_exceptions=base_adapter_exceptions)
    def connect(self) -> None:
        """Establish a database connection."""
        try:
            if not self.is_connected:
                self._connection = psycopg2.connect(
                    dsn=self._dsn.unicode_string(), *self.args, **self.kwargs
                )
                logger.info("Database connection established.")
        except psycopg2.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            self._connection = None

    @backoff(retry_exceptions=base_adapter_exceptions)
    @contextlib.contextmanager
    def cursor(self) -> "PostgresAdapterCursor":
        """Provide a transactional scope around a series of operations."""
        cursor = None
        if not self.is_connected:
            self.connect()
        try:
            cursor = PostgresAdapterCursor(self)
            logger.info(f"Cursor is opened: {cursor}")
            yield cursor
        finally:
            if cursor is not None:
                cursor.close()
                logger.info(f"Cursor is closed: {cursor}")

    def reconnect(self) -> None:
        super().reconnect()

    @backoff(retry_exceptions=base_adapter_exceptions)
    def close(self) -> None:
        super().close()

    @property
    def connection(self):
        return self._connection


class PostgresAdapterCursor(BaseAdapter):
    base_adapter_exceptions = psycopg2.OperationalError
    _cursor: pg_cursor

    def __init__(self, connection: PostgresAdapter, *args, **kwargs):
        self._connection = connection
        self.connect(*args, **kwargs)

    @property
    def is_cursor_opened(self) -> bool:
        return self._cursor and not self._cursor.closed

    @property
    def is_connection_opened(self) -> bool:
        return self._connection.is_connected

    @property
    def is_connected(self) -> bool:
        return self.is_connection_opened and self.is_cursor_opened

    @backoff(retry_exceptions=base_adapter_exceptions)
    def connect(self, *args, **kwargs) -> None:
        """Ensure the cursor is ready for use."""
        if not self.is_connection_opened:
            self._connection.connect()
        self._cursor: pg_cursor = self._connection.connection.cursor(
            cursor_factory=DictCursor, *args, **kwargs
        )
        logger.info("Cursor is opened: `%r.", self)

    def reconnect(self) -> None:
        if not self.is_connection_opened:
            logger.debug("Reconnecting connection: `%r.", self)
            self._connection.connect()

        if not self.is_cursor_opened:
            logger.debug("Reconnecting cursor: `%r.", self)
            self.connect()

    @backoff(retry_exceptions=base_adapter_exceptions)
    def close(self) -> None:
        """Close the cursor."""
        if self.is_cursor_opened:
            self._cursor.close()
            logger.debug("Cursor is closed: `%r.", self)

    @backoff(retry_exceptions=(base_adapter_exceptions, psycopg2.DatabaseError))
    @datastore_reconnect
    def execute(self, query: str | SQL, *args, **kwargs) -> None:
        self._cursor.execute(query, *args, **kwargs)

    @backoff(retry_exceptions=(base_adapter_exceptions, psycopg2.DatabaseError))
    @datastore_reconnect
    def fetchmany(self, chunk: int) -> list[Any]:
        return self._cursor.fetchmany(size=chunk)

    def __repr__(self):
        connection_status = "open" if self.is_connection_opened else "closed"
        cursor_status = "open" if self.is_cursor_opened else "closed"
        return f"<PostgresAdapterCursor connection_status={connection_status} cursor_status={cursor_status}>"
