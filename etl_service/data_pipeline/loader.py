from typing import Any

from etl_service.data_pipeline.interfaces.data_process_interface import (
    DataProcessInterface,
)
from etl_service.datastore_adapters.elasticsearch_adapter import ElasticsearchAdapter
from etl_service.utility.logger import setup_logging
from etl_service.utility.state_manager import State

logger = setup_logging()


class Loader(DataProcessInterface):
    def __init__(
        self,
        eks_conn: ElasticsearchAdapter,
        state: State,
        eks_index: str,
        batch_size: int,
    ):
        self.eks_conn = eks_conn
        self.state = state
        self.eks_index = eks_index
        self.batch_size = batch_size

    def process(self):
        """
        Load data from the database into the Elasticsearch index.
        Receives data from transformer.
        """

        saved_state = None

        try:
            while True:
                last_updated, data_in, index = yield
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
                    index=self.eks_index,
                    raise_on_exception=True,
                )

        except GeneratorExit:
            logger.debug("Loader: Load is finished: `%s`", self.state.key)
            if saved_state:
                logger.warning(
                    "Loader: Updating current state: `%s` with value: `%s`",
                    self.state.key,
                    saved_state,
                )
                self.state.set(str(saved_state))
                logger.debug("Loader end: state: `%s`", self.state.get())
