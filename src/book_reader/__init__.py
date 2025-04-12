"""Book Reader - A tool for converting books to audiobooks.

A tool that converts PDF files to audiobooks using OpenAI's Text-to-Speech API.
"""

import logging
import os
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

__version__ = "0.1.0"

# Example: Define a default value or handle it elsewhere
DEFAULT_VALUE = "some_default"

logger = logging.getLogger(__name__)


def get_setting(key: str, default: Optional[str] = None) -> str:
    """Retrieves a setting, ensuring it's not None."""
    value = os.getenv(key, default)
    if value is None:
        # Or raise an error if the setting is mandatory
        # raise ValueError(f"Environment variable {key} not set")
        warning_msg = f"Environment variable {key} not set, using default: {default}"
        logger.warning(warning_msg)
        return default if default is not None else ""  # Ensure str return
    return value
