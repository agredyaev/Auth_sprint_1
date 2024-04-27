import datetime
from typing import Callable, Generator, Optional

from etl_service.models.movies import Filmwork
from etl_service.utility.logger import setup_logging
from etl_service.data_pipeline.interfaces.data_process_interface import (
    DataProcessInterface,
)

logger = setup_logging()


class FilmworkTransformer(DataProcessInterface):
    def __init__(
        self,
        next_node: Callable[
            [],
            Generator[Optional[tuple[datetime.datetime, list[Filmwork]]], None, None],
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
                previous_node_output = yield
                if previous_node_output is None:
                    logger.debug("Transformer: No state data received, skipping")
                    continue

                last_updated, data_in = previous_node_output
                logger.debug(f"Transformer: state data received: {last_updated}")
                data_in: list[Filmwork]
                for row in data_in:
                    row.transform()
                event_handler.send((last_updated, data_in))
                logger.debug(f"Transformer: state data sent: {last_updated}")
        except GeneratorExit:
            logger.debug("Transformer ended processing")
