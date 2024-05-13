import datetime
import time
from contextlib import closing
from typing import Type

from psycopg2 import DatabaseError
from redis.exceptions import RedisError

from etl_service.data_pipeline.extractors.base_extractor import BaseExtractor
from etl_service.data_pipeline.loader import Loader
from etl_service.data_pipeline.transformer import Transformer
from etl_service.datastore_adapters.elasticsearch_adapter import ElasticsearchAdapter
from etl_service.datastore_adapters.postgres_adapter import PostgresAdapter
from etl_service.datastore_adapters.redis_adapter import RedisAdapter
from etl_service.utility.logger import setup_logging
from etl_service.utility.settings import Settings, settings
from etl_service.utility.state_manager import RedisStateManager, State

logging = setup_logging(logger_name=__name__)


def run_data_pipeline(
    config: Settings,
    extractor: Type[BaseExtractor],
    state_key: str,
    timeout: int = settings.general.etl_timeout,
):
    """
    Execute the Extract-Transform-Load workflow for processing movies data
    from PostgreSQL to Elasticsearch via a Redis-based state management system.

    :param config: Application settings
    :param extractor: Type of the extractor
    :param state_key: State key
    :param timeout: Timeout between state updates
    """
    try:
        with closing(PostgresAdapter(config.db.dsn)) as pg_conn, closing(
            ElasticsearchAdapter(config.eks.dsn)
        ) as eks_conn, closing(RedisAdapter(config.redis.dsn)) as redis_conn:
            pg_conn: PostgresAdapter
            eks_conn: ElasticsearchAdapter
            redis_conn: RedisAdapter

            logging.info(
                "Successfully established connections to PostgreSQL, Elasticsearch, and Redis."
            )

            state = State(RedisStateManager(redis_conn), state_key)

            if not state.exists():
                state.set(str(datetime.datetime.min))
                logging.info("Initialized state: %s", state.get())

            logging.debug("Current state: %s", state.get())

            loader = Loader(
                eks_conn=eks_conn,
                state=state,
                batch_size=config.eks.load_batch_size,
            )
            transformer = Transformer(
                next_node=loader.process(),
            )
            extractor = extractor(
                pg_conn=pg_conn,
                state=state,
                batch_size=config.db.extract_batch_size,
                next_node=transformer.process(),
            )

            while True:
                extractor.process()
                logging.info("Waiting for %s seconds for next state update", timeout)
                time.sleep(timeout)

    except DatabaseError as db_err:
        logging.exception("Database error occurred: %s", db_err)
    except RedisError as redis_err:
        logging.exception("Redis error occurred: %s", redis_err)
    except Exception as e:
        logging.exception("An unexpected error occurred: %s", e)
    finally:
        logging.warning("Processes completed or terminated.")
