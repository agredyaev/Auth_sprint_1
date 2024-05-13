from typing import Type

from etl_service.data_pipeline.extractors.base_extractor import BaseExtractor
from etl_service.models.genre import Genre


class GenreExtractor(BaseExtractor):
    def __init__(self, pg_conn, state, batch_size, next_node):
        super().__init__(pg_conn, state, batch_size, next_node)

    @property
    def _index(self) -> str | None:
        return "genres"

    @property
    def _query_filename(self) -> str | None:
        return "genres.sql"

    @property
    def _model_class(self) -> Type[Genre]:
        return Genre

