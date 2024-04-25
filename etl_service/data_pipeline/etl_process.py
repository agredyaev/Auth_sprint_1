import datetime
import time
from contextlib import closing
from typing import Type

from psycopg2 import DatabaseError, OperationalError
from psycopg2.extras import DictCursor

from extractors.base_extractor import BaseExtractor
from loader import FilmworkLoader
from transformer import FilmworkTransformer
from ..utility.state_manager import State, RedisStateManager
from ..datastore_adapters.elasticsearch_adapter import ElasticsearchAdapter
from ..datastore_adapters.postgres_adapter import PostgresAdapter
from ..datastore_adapters.redis_adapter import RedisAdapter
from ..utility.settings import Settings
from ..utility.logger import setup_logging


logging = setup_logging()


def etl_process(settings: Settings,
                extractor_type: Type[BaseExtractor],
                state_key: str,
                timeout: int = 3):
    """
    Execute the Extract-Transform-Load workflow for processing movies data
    from PostgreSQL to Elasticsearch via a Redis-based state management system.

    :param settings: Application settings
    :param extractor_type: Type of the extractor
    :param state_key: State key
    :param timeout: Timeout between state updates
    """
    try:
        with closing(PostgresAdapter(settings.db.dsn, cursor_factory=DictCursor)) as pg_conn, \
                closing(ElasticsearchAdapter(settings.eks.dsn)) as eks_conn, \
                closing(RedisAdapter(settings.redis.dsn)) as redis_conn:
            pg_conn: PostgresAdapter
            eks_conn: ElasticsearchAdapter
            redis_conn: RedisAdapter

            logging.info("Successfully connected to PostgreSQL, Elasticsearch, and Redis.")

            state = State(RedisStateManager(redis_conn), state_key)

            if not state.exists():
                state.set(str(datetime.datetime.min))
                logging.info("Initialized state: %s", state.get())

            loader = FilmworkLoader(
                eks_conn=eks_conn,
                state=state,
                eks_index=settings.eks_index,
                load_chunk=settings.eks.load_batch_size,
            )
            transformer = FilmworkTransformer(
                load_pipe=loader.load,
            )
            extractor = extractor_type(
                pg_conn=pg_conn,
                state=state,
                extract_chunk=settings.db.extract_batch_size,
                transform_pipe=transformer.transform,
            )
            while True:
                extractor.extract()
                time.sleep(timeout)

    except DatabaseError as db_err:
        logging.error("Database error occurred: %s", db_err)
    except OperationalError as op_err:
        logging.error("Operational error with database connection: %s", op_err)
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
    finally:
        logging.info("ETL process completed or terminated with errors.")
