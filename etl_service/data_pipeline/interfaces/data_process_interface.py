from abc import ABC, abstractmethod
from etl_service.utility.logger import setup_logging

logger = setup_logging()


class DataProcessInterface(ABC):
    """
    Defines the interface for data processing.
    """

    @abstractmethod
    def process(self):
        """
        This method takes in the data as input and performs some processing on it.
        """
        raise NotImplementedError
