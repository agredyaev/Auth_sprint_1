import logging
import logging.config


def setup_logging(
    logger_name: str = "logger", log_file: str = None, log_level: str = "DEBUG"
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
            "formatter": "standard",
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
                "standard": {
                    "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
                },
            },
            "handlers": handlers,
            "loggers": {
                "": {"handlers": ["default"], "level": log_level, "propagate": True},
            },
        }
    )

    return logging.getLogger(logger_name)
