from typing import Type

from etl_service.data_pipeline.extractors.base_extractor import BaseExtractor
from etl_service.models.movie import Filmwork


class FilmworkExtractor(BaseExtractor):
    def __init__(self, pg_conn, state, batch_size, next_node):
        super().__init__(pg_conn, state, batch_size, next_node)

    @property
    def _index(self) -> str:
        return "movies"

    @property
    def _query_filename(self) -> str:
        return "movies.sql"

    @property
    def _model_class(self) -> Type[Filmwork]:
        return Filmwork
