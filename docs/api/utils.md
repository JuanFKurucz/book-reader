# Utilities

This page documents the utility functions and helpers used in Book Reader.

## Configuration Utilities

```python
def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from a YAML file.

    Args:
        config_path: Optional path to the configuration file

    Returns:
        Dictionary containing configuration values

    Raises:
        ConfigError: If there's an error loading the configuration
    """

def get_config_value(
    key: str,
    default: Any = None,
    config: Optional[Dict[str, Any]] = None
) -> Any:
    """Get a configuration value with fallback to environment variables and defaults.

    Args:
        key: Configuration key
        default: Default value to use if key is not found
        config: Optional configuration dictionary

    Returns:
        Configuration value
    """
```

## File System Utilities

```python
def ensure_directory_exists(directory: str) -> None:
    """Ensure that a directory exists, creating it if necessary.

    Args:
        directory: Directory path

    Raises:
        IOError: If the directory cannot be created
    """

def is_pdf_file(filepath: str) -> bool:
    """Check if a file is a PDF.

    Args:
        filepath: Path to the file

    Returns:
        True if the file is a PDF, False otherwise
    """

def get_filename_without_extension(filepath: str) -> str:
    """Get the filename without extension from a filepath.

    Args:
        filepath: Path to the file

    Returns:
        Filename without extension
    """
```

## Text Processing Utilities

```python
def clean_text(text: str) -> str:
    """Clean and normalize text for TTS processing.

    Args:
        text: Text to clean

    Returns:
        Cleaned text
    """

def split_text_into_sentences(text: str) -> List[str]:
    """Split text into sentences.

    Args:
        text: Text to split

    Returns:
        List of sentences
    """

def truncate_text(text: str, max_length: int = 4000) -> str:
    """Truncate text to a maximum length while preserving sentence boundaries.

    Args:
        text: Text to truncate
        max_length: Maximum length in characters

    Returns:
        Truncated text
    """
```

## Logging Utilities

```python
def setup_logging(level: str = "info", log_file: Optional[str] = None) -> None:
    """Set up logging for the application.

    Args:
        level: Logging level ("debug", "info", "warning", "error")
        log_file: Optional path to log file
    """

def log_exception(exception: Exception, message: str = "An error occurred") -> None:
    """Log an exception with a custom message.

    Args:
        exception: The exception to log
        message: Custom message to include
    """
```

## Progress Utilities

```python
def create_progress_bar(
    total: int,
    description: str = "Processing",
    disable: bool = False
) -> Any:
    """Create a progress bar for tracking operations.

    Args:
        total: Total number of items
        description: Description text for the progress bar
        disable: Whether to disable the progress bar

    Returns:
        Progress bar object
    """

def update_progress_bar(
    progress_bar: Any,
    n: int = 1,
    description: Optional[str] = None
) -> None:
    """Update a progress bar.

    Args:
        progress_bar: Progress bar object
        n: Number of items to increment by
        description: Optional new description text
    """
```

## Error Handling Utilities

```python
def retry_operation(
    operation: Callable,
    max_retries: int = 3,
    retry_delay: float = 1.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Any:
    """Retry an operation with exponential backoff.

    Args:
        operation: Function to retry
        max_retries: Maximum number of retry attempts
        retry_delay: Initial delay between retries in seconds
        exceptions: Tuple of exceptions to catch and retry

    Returns:
        Result of the operation

    Raises:
        The last exception if all retries fail
    """
```

For complete implementation details of these utilities, please refer to the source code.
