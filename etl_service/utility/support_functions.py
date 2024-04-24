from logger import setup_logging
from typing import Any

logger = setup_logging()


def load_query_from_file(filename: str) -> Any:
    """Load SQL query from file."""
    try:
        with open(filename, 'r') as file:
            return file.read()
    except (FileNotFoundError, IOError):
        logger.error(f'File not found: {filename}')
        return None


def split_into_chunks(items: list[Any], chunk_size: int):
    """ Yield successive chunks from list of items. """
    if not items or not chunk_size:
        return []
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]



