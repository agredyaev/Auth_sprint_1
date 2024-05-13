import logging
import logging.config
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
    def format(self, record):
        log_fmt = FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, style="{")
        return formatter.format(record)


def setup_logging(
        logger_name: str = "logger", log_file: str = None, log_level: str = settings.general.log_level
) -> logging.Logger:
    """
    Setup logging configuration for the application and return a logger instance.
    :param logger_name: Name of the logger
    :param log_file: File to write logs to (optional)
    :param log_level: Log level (default: 'INFO')
    :return: Logger instance
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

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "custom": {
                    "()": CustomFormatter
                },
            },
            "handlers": handlers,
            "loggers": {
                "": {"handlers": ["default"], "level": log_level, "propagate": True},
                "uvicorn": {"handlers": ["default"], "level": log_level},
                "uvicorn.error": {"handlers": ["default"], "level": log_level},
                "uvicorn.access": {"handlers": ["default"], "level": log_level},
            },
        }
    )

    return logging.getLogger(logger_name)

