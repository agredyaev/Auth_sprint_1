import inspect
import sqlite3
from contextlib import contextmanager
from dataclasses import astuple, dataclass, is_dataclass
from typing import List, Tuple, Type

import models
import psycopg2
from models import BaseModel
from psycopg2.extras import DictCursor, execute_values


@contextmanager
def get_connections(sqllite, dsl):
    """
    Context manager for establishing database connections.
    Parameters:
    - sqllite: Database connection string for SQLite.
    - dsl: Dictionary of connection parameters for PostgreSQL.

    Yields:
    - Tuple containing the SQLite connection and the PostgreSQL connection.
    """
    sqlite_conn = sqlite3.connect(sqllite)
    pg_conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    try:
        yield sqlite_conn, pg_conn
    finally:
        pg_conn.close()
        sqlite_conn.close()


def get_dataclasses() -> List[Type[dataclass]]:
    """
    Retrieves a list of all dataclass types defined in the content_dataclasses module.
    The returned list is sorted to ensure that subclasses of Link are listed last.

    Returns:
        List[Type[dataclass]]: A list of dataclass types sorted by their inheritance from Link.
    """
    dataclasses_ = [
        obj for _, obj in inspect.getmembers(content_dataclasses, predicate=is_dataclass)
    ]
    return sorted(
        dataclasses_,
        key=lambda cls: issubclass(cls, content_dataclasses.Link)
    )


class BatchDataProcessor:
    """"
    Manages batch data migration from SQLite to PostgreSQL using model-defined SQL queries, handling transactions and conflicts."
    """

    def __init__(self, sqlite_conn: sqlite3.Connection,
                 pg_conn: psycopg2.extensions.connection, model_class: Type[BaseModel]):
        self.model_class = model_class
        self.model_class.check_fields_overridden()
        self.sqlite_conn = sqlite_conn
        self.sqlite_conn.row_factory = sqlite3.Row
        self.pg_conn = pg_conn
        self.batch_size = 10000

    def __create_queries(self) -> Tuple[str, str]:

        retrieved_fields = ','.join(self.model_class.retrieved_fields)

        query_to_retrieve = f"""
            SELECT {retrieved_fields} FROM {self.model_class.table_name}
        """
        
        inserted_fields = ','.join(self.model_class.get_own_fields())
        on_conflict = ','.join(self.model_class.constraints)

        query_to_insert = f"""
            INSERT INTO {self.model_class.schema}.{self.model_class.table_name} ({inserted_fields})
            VALUES %s
            ON CONFLICT ({on_conflict}) DO NOTHING;
        """

        return (query_to_retrieve, query_to_insert)

    def __fetch_batches(self, query_to_retrieve: str):
        cursor = self.sqlite_conn.cursor()
        cursor.execute(query_to_retrieve)
        while True:
            batch_data = cursor.fetchmany(self.batch_size)
            if not batch_data:
                break
            yield batch_data
        cursor.close()

    def load_batches(self) -> None:
        """
        Loads batches of data from the source database to the target database.
        Retrieves data using a predefined query, transforms each data row into an instance of model_class,
        and then inserts the data into the target database.
        Commits the transaction if successful or rolls back in case of an exception.
        """
        
        query_to_retrieve, query_to_insert = self.__create_queries()

        try:
            with self.pg_conn.cursor() as pg_cursor:

                for raw_data in self.__fetch_batches(query_to_retrieve):
                    batch_data = [astuple(self.model_class(**row))
                                  for row in raw_data]
                    execute_values(pg_cursor, query_to_insert, batch_data)

            self.pg_conn.commit()
        except Exception as e:
            self.pg_conn.rollback()
            error_message = f"An error occurred: {e}"
            raise type(e)(error_message).with_traceback(e.__traceback__) from None


