import logging
import logging.config
from typing import Any

from auth_service.src.core.config import settings

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DEFAULT_HANDLERS = [
    "console",
]
STREAM_HANDLER_CLASS = "logging.StreamHandler"


def get_log_config(log_file: str | None = None, log_level: str = settings.general.log_level) -> dict[str, Any]:
    """
    Return a logging configuration dictionary.
    :param log_file: File to write logs to (optional)
    :param log_level: Log level (default: 'INFO')
    :return: Logging configuration dictionary
    """
    handlers = {
        "console": {
            "level": log_level,
            "formatter": "default",
            "class": STREAM_HANDLER_CLASS,
        },
        "default": {
            "level": log_level,
            "formatter": "default",
            "class": STREAM_HANDLER_CLASS,
        },
        "access": {
            "level": log_level,
            "formatter": "access",
            "class": STREAM_HANDLER_CLASS,
        },
    }

    if log_file:
        handlers["file"] = {
            "level": log_level,
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": log_file,
            "mode": "a",
        }

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(levelprefix)s %(message)s",
                "class": "uvicorn.logging.DefaultFormatter",
            },
            "standard": {
                "format": LOG_FORMAT,
                "class": "logging.Formatter",
            },
            "verbose": {
                "format": LOG_FORMAT,
                "class": "logging.Formatter",
            },
            "access": {
                "format": "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
                "class": "uvicorn.logging.AccessFormatter",
            },
        },
        "handlers": handlers,
        "loggers": {
            "": {"handlers": LOG_DEFAULT_HANDLERS, "level": log_level},
            "uvicorn": {"level": log_level},
            "uvicorn.error": {"level": log_level},
            "uvicorn.access": {"handlers": ["access"], "level": log_level, "propagate": False},
        },
        "root": {
            "level": log_level,
            "formatter": "verbose",
            "handlers": LOG_DEFAULT_HANDLERS,
        },
    }


def setup_logging(
    logger_name: str = "logger", log_file: str | None = None, log_level: str = settings.general.log_level
) -> logging.Logger:
    """
    Setup logging configuration for the application and return a logger instance.
    :param logger_name: Name of the logger
    :param log_file: File to write logs to (optional)
    :param log_level: Log level (default: 'INFO')
    :return: Logger instance
    """
    logging.config.dictConfig(get_log_config(log_file, log_level))
    return logging.getLogger(logger_name)
