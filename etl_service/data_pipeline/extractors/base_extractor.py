import datetime
from typing import Any, Generator, List, Optional, Type

from abc import abstractmethod

from psycopg2.sql import SQL
from pydantic import BaseModel

from etl_service.datastore_adapters.postgres_adapter import (
    PostgresAdapter,
    PostgresAdapterCursor,
)
from etl_service.models.movies import Filmwork
from etl_service.models.state import UpdatedAtId
from etl_service.utility.logger import setup_logging
from etl_service.utility.state_manager import State
from etl_service.utility.support_functions import (
    apply_model_class,
    safe_format_sql_query,
)
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
            Optional[tuple[datetime.datetime, list[Filmwork]]], None, None
        ],
    ):
        self.state = state
        self.pg_conn = pg_conn
        self.batch_size = batch_size
        self.next_node = next_node
        self.proc_table: Optional[str] = None

    def _process_batches(
        self, cursor: PostgresAdapterCursor, query: SQL, items: List[Any]
    ) -> Generator[Any, None, None]:
        """Process a batch of data using the provided cursor and query."""
        try:
            cursor.execute(query, items)
            while results := cursor.fetchmany(self.batch_size):
                for result in results:
                    yield result
        except Exception as e:
            logger.exception("Error processing batch: %s", e)

    def _process_data_flow(
        self, query_filename: str, model_class: Type[BaseModel], next_handler: Generator
    ) -> Generator[None, None, None]:
        """
        Implements common logic for enrich and combined data flows.
        :param query_filename: Path to the SQL file.
        :param model_class: Model class
        :param next_handler: The next handler in the pipeline.
        """
        event_handler = next_handler
        next(event_handler)

        logger.debug("Processing of %s started", query_filename)

        with self.pg_conn.cursor() as cursor:
            try:
                while True:
                    last_updated, data_in = yield
                    logger.debug(
                        f"Processing of {query_filename}:state data received: {last_updated}"
                    )
                    data_in: List[UpdatedAtId]

                    batches = self._process_batches(
                        cursor=cursor,
                        query=safe_format_sql_query(
                            filename=query_filename, table_name=self.proc_table
                        ),
                        items=[
                            tuple([row.id for row in data_in])
                            if data_in
                            else tuple([None])
                        ],
                    )

                    data_out = [
                        apply_model_class(batch, model_class) for batch in batches
                    ]
                    event_handler.send((last_updated, data_out))
                    logger.debug(
                        f"Processing of {query_filename}: state data sent: {last_updated}"
                    )
            except GeneratorExit:
                logger.debug("Processing of %s ended", query_filename)

    def process(self):
        """
        Initializes the extraction process.
        Monitors the state of the data in the source database.
        Sends the state to the enriched data stage in the pipeline.
        """
        event_handler = self._enrich_data()
        next(event_handler)

        logger.debug(
            "Initialize processing %s: Start of data fetching", self.proc_table
        )

        with self.pg_conn.cursor() as cursor:
            try:
                batches = self._process_batches(
                    cursor=cursor,
                    query=safe_format_sql_query(
                        filename="fetch_changed_rows.sql",
                        table_name=self.proc_table,
                    ),
                    items=[self.state.get().updated_at],
                )

                data_out = [apply_model_class(batch, UpdatedAtId) for batch in batches]
                if not data_out:
                    logger.info(
                        f"Fetch data: No changed rows to process, sent: state:{None}:data_out:{[]}"
                    )
                    event_handler.send((None, []))
                    return

                last_updated = data_out[-1].updated_at
                event_handler.send((last_updated, data_out))

                logger.debug(
                    "Fetch data: %s state %s data sent", self.proc_table, last_updated
                )
            except GeneratorExit:
                logger.debug("%s: End of data fetching", self.proc_table)

    @property
    @abstractmethod
    def _enrich_data_query(self) -> Optional[str]:
        """
        Defines query for enriching data in the source database.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def _enrich_data(self):
        """
        Enriches the data in the source database.
        Sends the enriched data to the combined data stage in the pipeline.
        """
        return self._process_data_flow(
            query_filename=self._enrich_data_query,
            model_class=UpdatedAtId,
            next_handler=self._combine_data(),
        )

    def _combine_data(self):
        """
        Combines corresponding data for the changed rows.
        Sends the combined data to the next node in the pipeline.
        """
        return self._process_data_flow(
            query_filename="combine_data_changed_rows.sql",
            model_class=Filmwork,
            next_handler=self.next_node,
        )
