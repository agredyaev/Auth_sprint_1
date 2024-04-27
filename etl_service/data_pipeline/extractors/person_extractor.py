from etl_service.data_pipeline.extractors.base_extractor import BaseExtractor


class PersonExtractor(BaseExtractor):
    def __init__(self, pg_conn, state, batch_size, next_node):
        super().__init__(pg_conn, state, batch_size, next_node)
        self.proc_table = "person"

    @property
    def _enrich_data_query(self):
        return "enrich_changed_rows.sql"
