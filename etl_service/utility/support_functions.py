from importlib import resources
from typing import Any, Generator, Optional, Type

from psycopg2.sql import SQL
from pydantic import BaseModel

from etl_service.utility.logger import setup_logging
from etl_service.utility.settings import settings

logger = setup_logging(logger_name=__name__)


def load_query_from_file(filename: str) -> Optional[str]:
    """Load SQL query from file.

    :param filename: Path to the SQL file relative to the package.
    :return: A string containing the SQL query, or None if an error occurs.
    """
    sql_package = f"{settings.general.package_name}.sql"
    try:
        return resources.read_text(sql_package, filename)
    except (FileNotFoundError, IOError):
        logger.error("File %s not found in package %s ", filename, sql_package)
        return None


def safe_format_sql_query(filename: str) -> SQL | None:
    """
    Load a SQL query template from a file, then safely format it using psycopg2.sql.

    :param filename: Path to the SQL file.
    :return: A psycopg2.sql.SQL object ready for execution, or None if an error occurs.
    """
    query_template_str = load_query_from_file(filename)
    if not query_template_str:
        logger.error("Couldn't load query from file: %s", filename)
        return None

    try:
        query_template = SQL(query_template_str)

        return query_template
    except Exception as e:
        logger.error("Failed to format the SQL query: %s", e)
        return None


def apply_model_class(row: dict[str, Any], model_class: Type[BaseModel]) -> dict[str, Any]:
    """
    Apply Model class to results.
    :param row: Dictionary of results
    :param model_class: Model class
    :return: Dictionary of results
    """
    return model_class(**row).model_dump(by_alias=True)


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
        yield items[i : i + chunk_size]
