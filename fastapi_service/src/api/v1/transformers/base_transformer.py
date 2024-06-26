from abc import ABC, abstractmethod
from typing import Any


class BaseTransformer(ABC):
    @abstractmethod
    def to_response(self, *args: Any, **kwargs: Any) -> Any:
        """
        This method takes in the data as input and performs some processing on it.
        """
        raise NotImplementedError

    def to_response_list(self, model_list: list[Any]) -> list[Any]:
        """
        This method takes in the data as input and performs some processing on it.

        :param model_list: List of BaseModel objects to transform.
        :return: List of transformed objects.

        """
        return [self.to_response(model) for model in model_list]
