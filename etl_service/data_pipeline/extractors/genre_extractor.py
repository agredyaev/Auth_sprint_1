from base_extractor import BaseExtractor


class GenreExtractor(BaseExtractor):
    def __init__(self, pg_conn, state, batch_size, next_node):
        super().__init__(pg_conn, state, batch_size, next_node)
        self.proc_table = "genre"

    @property
    def _enrich_data_query(self):
        return './sql/enrich_changed_rows.sql'

