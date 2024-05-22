from typing import Type

from etl_service.data_pipeline.extractors.base_extractor import BaseExtractor
from etl_service.models.person import Person


class PersonExtractor(BaseExtractor):
    def __init__(self, pg_conn, state, batch_size, next_node):
        super().__init__(pg_conn, state, batch_size, next_node)

    @property
    def _index(self) -> str:
        return "people"

    @property
    def _query_filename(self) -> str:
        return "people.sql"

    @property
    def _model_class(self) -> Type[Person]:
        return Person
