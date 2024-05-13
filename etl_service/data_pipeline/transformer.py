import datetime
from typing import Callable, Generator, Optional

from psycopg2.extras import DictRow
from pydantic import BaseModel

from etl_service.utility.logger import setup_logging
from etl_service.data_pipeline.interfaces.data_process_interface import (
    DataProcessInterface,
)
from etl_service.utility.support_functions import apply_model_class

logger = setup_logging()


class Transformer(DataProcessInterface):
    def __init__(
            self,
            next_node: Callable[
                [],
                Generator[Optional[list[BaseModel]], None, None],
            ],
    ):
        self.next_node = next_node

    def process(self):
        """
        This method handles the transformation of raw film data into a structured format,
        preparing it for loading into data storage systems. The transformation involves
        cleaning, formatting, and enriching the data attributes.
        """

        event_handler = self.next_node
        next(event_handler)

        logger.debug("Transformer: started processing")

        try:
            while True:
                previous_node_output = (yield)
                if previous_node_output is None:
                    logger.debug("Transformer: No state data received, skipping")
                    continue

                last_updated, data_in, index, model_class = previous_node_output
                data_in: list[DictRow]

                logger.debug(f"Transformer: state data received {index}, {last_updated}")

                data_out = [apply_model_class(row, model_class) for row in data_in]

                event_handler.send((last_updated, data_out, index))

                logger.debug(f"Transformer: state data sent: {index}, {last_updated}")
        except GeneratorExit:
            logger.debug("Transformer ended processing")
