from base_extractor import BaseExtractor


class FilmworkExtractor(BaseExtractor):
    def __init__(self, pg_conn, state, batch_size, next_node):
        super().__init__(pg_conn, state, batch_size, next_node)
        self.proc_table = "film_work"

    @property
    def _enrich_data_query(self):
        return None

    def _enrich_data(self):
        """
        Overrides parent method
        """
        event_handler = self._merge()
        next(event_handler)

        try:
            while True:
                last_updated, rows = (yield)
                event_handler.send((last_updated, rows))

        except GeneratorExit:
            pass
