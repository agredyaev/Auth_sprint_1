from typing import Any

from etl_service.data_pipeline.interfaces.data_process_interface import (
    DataProcessInterface,
)
from etl_service.datastore_adapters.elasticsearch_adapter import ElasticsearchAdapter
from etl_service.utility.logger import setup_logging
from etl_service.utility.state_manager import State

logger = setup_logging(logger_name=__name__)


class Loader(DataProcessInterface):
    def __init__(
        self,
        eks_conn: ElasticsearchAdapter,
        state: State,
        batch_size: int,
    ):
        self.eks_conn = eks_conn
        self.state = state
        self.batch_size = batch_size

    def process(self):
        """
        Load data from the database into the Elasticsearch index.
        Receives data from transformer.
        """

        saved_state = None

        try:
            while True:
                previous_node_output = yield
                if previous_node_output is None:
                    logger.debug("Loader: No changed rows to process, skipping")
                    continue

                last_updated, data_in, index = previous_node_output
                data_in: list[dict[str, Any]]
                logger.debug(f"Loader start:state data received: {index}, {last_updated}")

                if not saved_state:
                    saved_state = last_updated
                elif saved_state != last_updated:
                    logger.warning(
                        ",Loader: State is changed. Updating current state: `%s` with value: `%s`",
                        self.state.key,
                        saved_state,
                    )
                    self.state.set(str(saved_state))
                    saved_state = last_updated

                data_out = [
                    {
                        "_index": index,
                        "_op_type": "index",
                        "_id": row.get("id"),
                        "_source": row,
                    }
                    for row in data_in
                ]

                self.eks_conn.chunked_bulk(
                    items=data_out,
                    batch_size=self.batch_size,
                    index=index,
                    raise_on_exception=True,
                )

                if saved_state:
                    logger.warning(
                        "Loader: Updating current state: `%s` with value: `%s`",
                        self.state.key,
                        saved_state,
                    )
                    self.state.set(str(saved_state))
                    logger.debug("Loader end: state: `%s`", self.state.get())

        except GeneratorExit:
            logger.info("Loader: Load is finished: `%s`", self.state.key)
