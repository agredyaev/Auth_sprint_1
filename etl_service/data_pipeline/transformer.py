import datetime
from typing import Callable, Generator

from ..utility.logger import setup_logging
from ..models.movies import Filmwork

logger = setup_logging()


class FilmworkTransformer:
    def __init__(
        self,
        next_node: Callable[[], Generator[None, tuple[datetime.datetime, list[Filmwork]] | None, None]]
    ):
        self.next_node = next_node

    def transform(self):
        """
        Implements the transformation process.
        """
        global last_updated
        event_handler = self.next_node()
        next(event_handler)

        try:
            while True:
                last_updated, data_in = yield
                rows: list[Filmwork]
                for row in data_in:
                    row.transform()

                event_handler.send((last_updated, data_in))
        except GeneratorExit:
            logger.debug(
                "Transformer finished with last_updated: %s",
                last_updated
            )
