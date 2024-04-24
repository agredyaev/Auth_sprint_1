from logger import setup_logging
from typing import Any, Optional, Generator, List, Type
from psycopg2.sql import SQL, Identifier
from pydantic import BaseModel


logger = setup_logging()


def load_query_from_file(filename: str) -> Optional[str] | None:
    """Load SQL query from file.

    :param filename: Path to the SQL file.
    :return: A string containing the SQL query, or None if an error occurs.
    """
    try:
        with open(filename, 'r') as file:
            return file.read()
    except (FileNotFoundError, IOError):
        logger.error(f'File not found: {filename}')
        return None


def safe_format_sql_query(filename: str, table_name: str) -> SQL | None:
    """
    Load a SQL query template from a file, then safely format it using psycopg2.sql.

    :param filename: Path to the SQL file.
    :param table_name: Name of the table in the database.
    :return: A psycopg2.sql.SQL object ready for execution, or None if an error occurs.
    """
    query_template_str = load_query_from_file(filename)
    if not query_template_str:
        logger.error("Couldn't load query from file: %s", filename)
        return None

    try:
        query_template = SQL(query_template_str)
        formatted_query = query_template.format(table_name=Identifier(table_name))
        return formatted_query
    except Exception as e:
        logger.error("Failed to format the SQL query: %s", e)
        return None


def apply_model_class(results: List[Any], model_class: Type[BaseModel]) -> List[BaseModel]:
    """
    Apply Model class to results.
    :param results: List of results
    :param model_class: Model class
    :return: List of Model class instances
    """
    return [model_class(**result) for result in results]



def split_into_chunks(items: list[Any], chunk_size: int) -> Generator[list[Any], None, None]:
    """
    Yield successive chunks from list of items.

    :param items: List of items
    :param chunk_size: Size of each chunk
    :return: Generator of chunks
    """
    if not items or not chunk_size:
        return []
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]
