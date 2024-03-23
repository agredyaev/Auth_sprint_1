import backoff
import psycopg2
from psycopg2 import extras

class PostgresExtractor:
    def __init__(self, dsn, table_name, state_manager):
        self.dsn = dsn
        self.table_name = table_name
        self.state_manager = state_manager
        self.connection = self.connect_to_db()

    @backoff.on_exception(backoff.expo, psycopg2.OperationalError, max_time=300)
    def connect_to_db(self):
        return psycopg2.connect(self.dsn)

    def fetch_next_batch(self, batch_size=100):
        last_processed_id = self.state_manager.load_state().get(self.table_name, 0)
        query = f"SELECT * FROM {self.table_name} WHERE id > %s ORDER BY id LIMIT %s;"
        with self.connection.cursor(cursor_factory=extras.DictCursor) as cursor:
            cursor.execute(query, (last_processed_id, batch_size))
            records = cursor.fetchall()
        if records:
            self.state_manager.save_state({self.table_name: records[-1]['id']})
        return records
