"""Configuration settings for Book Reader."""

import logging
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings

# Configure logger
logger = logging.getLogger(__name__)


def _get_cpu_count() -> int:
    """Return max(1, cpu_count) to ensure at least 1 task."""
    cpu_count = os.cpu_count() or 1
    return max(1, cpu_count)


def get_env_path() -> Optional[Path]:
    """Get the path to the .env file, searching common locations."""
    # ... (existing function) ...


# Load environment variables from .env file if it exists
env_path = get_env_path()
if env_path:
    load_dotenv(dotenv_path=env_path)
else:
    print("Warning: .env file not found. Using system environment variables.")


class AudioSettings(BaseSettings):
    """Audio settings for TTS conversion."""

    model: str = Field(default="tts-1", description="TTS model to use")
    voice: str = Field(default="alloy", description="Voice for TTS")
    max_text_length: int = Field(
        default=4000, description="Max length for text chunks sent to TTS API"
    )
    concurrent_tasks: int = Field(
        default=4,
        validation_alias="CONCURRENT_TASKS",
        description="Number of concurrent TTS tasks",
    )


class PathSettings(BaseSettings):
    """Path settings for various directories and files."""

    books_dir: Path = Field(
        default=Path("./books"), description="Directory for input PDF files"
    )
    output_dir: Path = Field(
        default=Path("./audiobooks"), description="Directory for output audio files"
    )
    temp_dir: Path = Path("temp")
    log_file: Path = Path("book_reader.log")
    progress_file: Path = Field(
        default=Path("./book_reader_progress.json"),
        description="File to store conversion progress",
    )


class Settings(BaseSettings):
    """Main settings class for the application."""

    openai_api_key: str = Field(
        default="",  # Default to empty string instead of required
        description="OpenAI API Key",
    )
    log_level: str = Field(
        default="INFO", validation_alias="LOG_LEVEL", description="Logging level"
    )
    audio: AudioSettings = AudioSettings()
    paths: PathSettings = PathSettings()
    batch_size: int = Field(
        default=4,
        validation_alias="BOOK_READER_BATCH_SIZE",
        description="Chunks to process in parallel",
    )
    debug: bool = False

    @field_validator("openai_api_key")
    @classmethod
    def check_api_key(cls, value: str) -> str:
        if not value:
            # Just warn instead of raising an error during tests
            logger.warning("OPENAI_API_KEY environment variable is not set.")
        return value

    @field_validator("log_level")
    @classmethod
    def check_log_level(cls, value: str) -> str:
        value = value.upper()
        if value not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError(f"Invalid LOG_LEVEL: {value}")
        return value


# Load settings and handle potential errors
try:
    # Get API key from environment
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    settings = Settings(openai_api_key=openai_api_key)
except ValidationError as e:
    print(f"Error loading settings: {e}")
    # Exit or raise depending on desired behavior
    raise SystemExit(1) from e

# Override with environment variables if available
# Use getenv with defaults or check for None before assigning/casting
voice_env = os.getenv("BOOK_READER_VOICE")
if voice_env is not None:
    settings.audio.voice = voice_env

model_env = os.getenv("BOOK_READER_MODEL")
if model_env is not None:
    settings.audio.model = model_env

max_text_length_env = os.getenv("BOOK_READER_MAX_TEXT_LENGTH")
if max_text_length_env is not None:
    try:
        settings.audio.max_text_length = int(max_text_length_env)
    except ValueError:
        logger.warning("Invalid BOOK_READER_MAX_TEXT_LENGTH, using default.")

books_dir_env = os.getenv("BOOK_READER_BOOKS_DIR")
if books_dir_env is not None:
    settings.paths.books_dir = Path(books_dir_env)

output_dir_env = os.getenv("BOOK_READER_OUTPUT_DIR")
if output_dir_env is not None:
    settings.paths.output_dir = Path(output_dir_env)

progress_file_env = os.getenv("BOOK_READER_PROGRESS_FILE")
if progress_file_env is not None:
    settings.paths.progress_file = Path(progress_file_env)

batch_size_env = os.getenv("BOOK_READER_BATCH_SIZE")
if batch_size_env is not None:
    try:
        settings.batch_size = int(batch_size_env)
    except ValueError:
        msg = "Invalid BOOK_READER_BATCH_SIZE, using default: {} "
        logger.warning(msg.format(settings.batch_size))

debug_env = os.getenv("BOOK_READER_DEBUG")
if debug_env is not None:
    debug_value = debug_env.lower()
    settings.debug = debug_value in ("true", "1", "yes")

log_file_env = os.getenv("BOOK_READER_LOG_FILE")
if log_file_env is not None:
    settings.paths.log_file = Path(log_file_env)
