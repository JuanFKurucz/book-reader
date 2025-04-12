"""Logging utility for the PDF to Audiobook converter."""

import logging
from typing import Any

from book_reader.config.settings import settings

# Define LOG_LEVELS if not already defined
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def setup_logging() -> None:
    """Configure logging based on settings."""
    log_level_name = settings.log_level.upper()
    log_level = LOG_LEVELS.get(log_level_name, logging.INFO)

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_date_format = "%Y-%m-%d %H:%M:%S"

    # Ensure log directory exists
    log_dir = settings.paths.log_file.parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # Basic configuration with file and console handlers
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=log_date_format,
        handlers=[
            logging.FileHandler(settings.paths.log_file),
            logging.StreamHandler(),  # Log to console as well
        ],
    )

    # Optionally silence noisy libraries
    # logging.getLogger("some_library").setLevel(logging.WARNING)

    logger = get_logger(__name__)  # Get logger after setup
    logger.info(f"Logging initialized with level: {log_level_name}")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name."""
    return logging.getLogger(name)


# Convenience functions (ensure they use the configured logger)
# Consider moving these or using the logger directly where needed


def debug(msg: str, *args: Any, **kwargs: Any) -> None:
    logging.debug(msg, *args, **kwargs)


def info(msg: str, *args: Any, **kwargs: Any) -> None:
    logging.info(msg, *args, **kwargs)


def warning(msg: str, *args: Any, **kwargs: Any) -> None:
    logging.warning(msg, *args, **kwargs)


def error(msg: str, *args: Any, **kwargs: Any) -> None:
    logging.error(msg, *args, **kwargs)


def critical(msg: str, *args: Any, **kwargs: Any) -> None:
    logging.critical(msg, *args, **kwargs)
