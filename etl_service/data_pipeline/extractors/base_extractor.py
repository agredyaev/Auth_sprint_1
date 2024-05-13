import datetime
from typing import Any, Generator, List, Optional, Type

from abc import abstractmethod

from psycopg2.extras import DictRow
from psycopg2.sql import SQL
from pydantic import BaseModel

from etl_service.datastore_adapters.postgres_adapter import (
    PostgresAdapter,
    PostgresAdapterCursor,
)
from etl_service.utility.logger import setup_logging
from etl_service.utility.state_manager import State
from etl_service.utility.support_functions import safe_format_sql_query
from etl_service.data_pipeline.interfaces.data_process_interface import (
    DataProcessInterface,
)

logger = setup_logging()


class BaseExtractor(DataProcessInterface):
    def __init__(
            self,
            pg_conn: PostgresAdapter,
            state: State,
            batch_size: int,
            next_node: Generator[
                Optional[tuple[Type[datetime.datetime], list[DictRow], str, str]], None, None
            ],
    ):
        self.state = state
        self.pg_conn = pg_conn
        self.batch_size = batch_size
        self.next_node = next_node

    def _process_batches(
            self, cursor: PostgresAdapterCursor, query: SQL, **kwargs
    ) -> Generator[Any, None, None]:
        """Process a batch of data using the provided cursor and query."""
        try:
            cursor.execute(query, **kwargs)
            while results := cursor.fetchmany(self.batch_size):
                for result in results:
                    yield result
        except Exception as e:
            logger.exception("Error processing batch: %s", e)

    def process(self):
        """
        Initializes the extraction process.
        Monitors the state of the data in the source database.
        Sends the state to the enriched data stage in the pipeline.
        """
        event_handler = self.next_node
        next(event_handler)

        logger.debug(
            "Initialize processing %s: Start of data fetching", self._index
        )

        with self.pg_conn.cursor() as cursor:
            try:
                batches = self._process_batches(
                    cursor=cursor,
                    query=safe_format_sql_query(
                        filename=self._query_filename
                    ),
                    params={'updated_at': self.state.get().updated_at},
                )

                data_out = [dict(batch) for batch in batches]
                if not data_out:
                    logger.info(
                        f"Fetch data: No changed rows to process, sent: state:{None}:data_out:{[]}"
                    )
                    event_handler.send((None, [], None, None))
                    return
                last_updated = data_out[-1].get("updated_at")
                event_handler.send((last_updated, data_out, self._index, self._model_class))

                logger.debug(
                    "Fetch data: %s state %s data sent", self._index,
                )
            except GeneratorExit:
                logger.debug("%s: End of data fetching", self._index)

    @property
    @abstractmethod
    def _query_filename(self) -> str | None:
        raise NotImplementedError("Subclasses must implement _query_filename property.")

    @property
    @abstractmethod
    def _index(self) -> str | None:
        raise NotImplementedError("Subclasses must implement _index property.")

    @property
    @abstractmethod
    def _model_class(self) -> Type[BaseModel] | None:
        raise NotImplementedError("Subclasses must implement _model_class property.")
