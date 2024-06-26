# src/core/logger.py
import logging
import logging.config
from typing import Any

from fastapi_service.src.core.config import settings

FMT = "[{levelname:^7}] {name}: {message}"

FORMATS = {
    logging.DEBUG: f"\33[38m{FMT}\33[0m",
    logging.INFO: f"\33[36m{FMT}\33[0m",
    logging.WARNING: f"\33[33m{FMT}\33[0m",
    logging.ERROR: f"\33[31m{FMT}\33[0m",
    logging.CRITICAL: f"\33[1m\33[31m{FMT}\33[0m",
}


class CustomFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_fmt = FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, style="{")
        return formatter.format(record)


def get_log_config(log_file: str | None = None, log_level: str = settings.general.log_level) -> dict[str, Any]:
    """
    Return a logging configuration dictionary.
    :param log_file: File to write logs to (optional)
    :param log_level: Log level (default: 'INFO')
    :return: Logging configuration dictionary
    """
    handlers = {
        "default": {
            "level": log_level,
            "formatter": "custom",
            "class": "logging.StreamHandler",
        }
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
            "custom": {"()": CustomFormatter},
        },
        "handlers": handlers,
        "loggers": {
            "": {"handlers": ["default"], "level": log_level},
            "uvicorn": {"level": log_level},
            "uvicorn.error": {"level": log_level},
            "uvicorn.access": {"handlers": ["default"], "level": log_level, "propagate": False},
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
