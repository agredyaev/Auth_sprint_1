import asyncio
from abc import ABC, abstractmethod
from typing import Optional, Callable, Generator, Any

from psycopg2.sql import SQL, Identifier

from ...utility.decorators import coroutine
from ...utility.logger import setup_logging
from ...utility.state_manager import State
from ...utility.support_functions import load_query_from_file
from ...models.state import UpdatedAtId
from ...models.movies import Filmwork
from ...datastore_adapters.postgres_adapter import PostgresAdapter

logger = setup_logging()


class BaseExtractor(ABC):
    def __init__(self, pg_conn: PostgresAdapter, state: State, extract_chunk: int):
        self.state = state
        self.pg_conn = pg_conn
        self.extract_chunk = extract_chunk
        self.produce_table: Optional[str] = None

    def extract(self):
        """Start pipeline: [produce -> enrich -> merge]."""
        self._produce()

    @coroutine
    def _execute_and_pass_data(self, sql_query: SQL, data_processor: Callable[[list], Any], next_stage: Generator):
        """Coroutine to execute a SQL query and pass data to the next stage."""
        try:
            with self.pg_conn.cursor() as cur:
                cur.execute(sql_query, [self.state.get().updated_at])
                while results := cur.fetchmany(self.extract_chunk):
                    processed_data = data_processor(results)
                    next_stage.send(processed_data)
                    logger.info("Data processed and sent to the next stage.")
        except Exception as e:
            logger.error(f"An error occurred during SQL execution or data processing: {e}")

    @coroutine
    def _produce(self):
        """Coroutine to monitor data update in PGSQL. Send data to enricher."""
        sql_query = SQL("SELECT id, updated_at FROM content.{} WHERE updated_at > %s ORDER BY updated_at;").format(
            Identifier(self.produce_table))
        yield from self._execute_and_pass_data(sql_query, self._process_produce_data, self._enrich)

    def _process_produce_data(self, data: list) -> list:
        """Process data fetched by _produce."""
        return [UpdatedAtId(**result) for result in data]

    @abstractmethod
    @coroutine
    def _enrich(self):
        """Coroutine to enrich data. Send data to merger."""
        pass

    @abstractmethod
    @coroutine
    def _merge(self):
        """Coroutine to merge data. Send data to transformer."""
        pass
