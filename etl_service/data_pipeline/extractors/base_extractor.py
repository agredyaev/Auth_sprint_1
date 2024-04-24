import datetime
from abc import ABC, abstractmethod
from typing import Optional, Callable, Generator, Any, List, Tuple, Type

from pydantic import BaseModel
from psycopg2.sql import SQL

from ...utility.logger import setup_logging
from ...utility.state_manager import State
from ...utility.support_functions import safe_format_sql_query, apply_model_class
from ...models.state import UpdatedAtId
from ...models.movies import Filmwork
from ...datastore_adapters.postgres_adapter import PostgresAdapter, PostgresAdapterCursor

logger = setup_logging()


class BaseExtractor(ABC):
    def __init__(
            self,
            pg_conn: PostgresAdapter,
            state: State,
            batch_size: int,
            next_node: Generator[None, tuple[datetime.datetime, list[Filmwork]] | None, None]
    ):
        self.state = state
        self.pg_conn = pg_conn
        self.batch_size = batch_size
        self.next_node = next_node
        self.proc_table: Optional[str] = None

    def _process_batches(self,
                         cursor: PostgresAdapterCursor,
                         query: SQL,
                         items: List[Any]
                         ) -> Generator[Any, None, None]:
        """ Process a batch of data using the provided cursor and query. """
        try:
            cursor.execute(query, items)
            while results := cursor.fetchmany(self.batch_size):
                for result in results:
                    yield result
        except Exception as e:
            logger.error("Error processing batch: %s", e)

    def _process_data_flow(self, query_filename: str, model_class: Type[BaseModel], next_handler: Callable):
        """
        Implements common logic for enrich and combined data flows.
        :param query_filename: Path to the SQL file.
        :param model_class: Model class
        :param next_handler: The next handler in the pipeline.
        """
        event_handler = next_handler()
        next(event_handler)

        with self.pg_conn.cursor() as cursor:
            try:
                while True:
                    last_updated, data_in = yield
                    data_in: List[UpdatedAtId]

                    batches = self._process_batches(
                        cursor=cursor,
                        query=safe_format_sql_query(
                            filename=query_filename,
                            table_name=self.proc_table
                        ),
                        items=[tuple([row.id for row in data_in])]
                    )

                    data_out = [apply_model_class(batch, model_class) for batch in batches]
                    event_handler.send((last_updated, data_out))
            except GeneratorExit:
                event_handler.close()
                logger.debug("End of processing: %s", query_filename.split('-')[0])

    def extract(self):
        """
        Initializes the extraction process.
        """
        self._fetch_data()

    def _fetch_data(self):
        """
        Monitors the state of the data in the source database.
        Sends the state to the enriched data stage in the pipeline.
        """
        event_handler = self._enrich_data()
        next(event_handler)

        with self.pg_conn.cursor() as cursor:
            try:
                batches = self._process_batches(
                    cursor=cursor,
                    query=safe_format_sql_query(
                        filename='./sql/fetch_changed_rows.sql',
                        table_name=self.proc_table
                    ),
                    items=[self.state.get().updated_at]
                )

                data_out = [apply_model_class(batch, UpdatedAtId) for batch in batches]
                last_updated = data_out[-1].updated_at
                event_handler.send((last_updated, data_out))
            except GeneratorExit:
                event_handler.close()
                logger.debug("End of data fetching")

    @property
    @abstractmethod
    def _enrich_data_query(self) -> str | None:
        """
        Defines query for enriching data in the source database.
        """
        return NotImplementedError

    def _enrich_data(self):
        """
        Enriches the data in the source database.
        Sends the enriched data to the combined data stage in the pipeline.
        """
        return self._process_data_flow(
            query_filename=self._enrich_data_query,
            model_class=UpdatedAtId,
            next_handler_generator=self._combine_data
        )

    def _combine_data(self):
        """
        Combines corresponding data for the changed rows.
        Sends the combined data to the next node in the pipeline.
        """
        return self._process_data_flow(
            query_filename='./combine_data_changed_rows.sql',
            model_class=Filmwork,
            next_handler_generator=self.next_node
        )
