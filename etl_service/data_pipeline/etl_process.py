import os

from dotenv import load_dotenv
from etl_service.utility.utils import BatchDataProcessor, get_connections, get_dataclasses

load_dotenv()


if __name__ == '__main__':
    dsl = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')}
    sqllite = os.getenv('DB_PATH')

    dataclasses = get_dataclasses()

    with get_connections(sqllite, dsl) as (sqlite_conn, pg_conn):
        for dataclass in dataclasses:
            processor = BatchDataProcessor(sqlite_conn, pg_conn, dataclass)
            processor.load_batches()
