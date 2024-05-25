from typing import Any

from faker import Faker
from pydantic import BaseModel


class BaseEntity:
    def __init__(self, id_: str, fake: Faker, num: int = 2) -> None:
        self._id = id_
        self._fake = fake
        self._num = num

    @property
    def model_attributes(self) -> dict[str, Any]:
        return {}

    def create_uuids_and_names_list(self, names: list[str] | None, model: type[BaseModel]) -> list[BaseModel]:
        if not names:
            return []
        return [model(id=str(self._fake.uuid4()), name=name) for name in names]

    def _create_single_entity(self, model: type[BaseModel], entity_id: str | None = None) -> BaseModel:
        attributes = self.model_attributes.copy()
        attributes.update({"id": entity_id if entity_id else self._fake.uuid4()})
        return model(**attributes)

    def _create_entities_list(self, numi: int, model: type[BaseModel]) -> list[BaseModel]:
        return [self._create_single_entity(model=model) for _ in range(numi)]

    def _get_entities_list(self, model: type[BaseModel]) -> list[BaseModel]:
        return self._create_entities_list(numi=(self._num - 1), model=model)

    def generate_data(self, model: type[BaseModel]) -> list[dict[str, Any]]:
        model_data = self._get_entities_list(model=model)
        model_data.append(self._create_single_entity(model=model, entity_id=self._id))
        return [model.model_dump() for model in model_data]
