# Book Reader

A modern, well-structured Python tool that converts PDF files to audiobooks using OpenAI's Text-to-Speech API.

## Project Overview

The core idea behind Book Reader is to provide an accessible and efficient way to transform written PDF content into listenable audio formats. Leveraging powerful AI tools like OpenAI's TTS, the project aims to make long documents, books, or articles more convenient to consume, especially for visually impaired users or during activities like commuting or exercising.

The project emphasizes:
- **Modularity:** Clear separation between text extraction, AI interaction, and CLI components.
- **Efficiency:** Parallel processing to speed up the conversion of large documents.
- **User Experience:** A straightforward command-line interface with clear feedback and options.
- **Resilience:** The ability to resume interrupted conversions.

## Current Status

The application currently implements the core PDF-to-audiobook pipeline. Key implemented functionalities include:
- PDF parsing and text extraction using PyMuPDF.
- Text preprocessing and chunking for the TTS API.
- Interaction with OpenAI's TTS API (supporting different models and voices).
- Parallel execution of TTS requests for performance.
- Saving generated audio segments and tracking progress.
- A command-line interface (CLI) built with Click and Rich for user interaction.
- Docker support for easy deployment and execution.

## Features

- Extract text from PDF files
- Convert text to high-quality audio using OpenAI's TTS API
- Process PDFs page by page
- Split text into manageable chunks
- Parallel processing for faster conversion
- Resume incomplete conversions
- User-friendly command-line interface with rich formatting
- Option to limit pages for testing purposes
- Support for different OpenAI TTS models and voices
- Uses the latest OpenAI SDK (≥1.0.0)
- Robust error handling and logging

## Requirements

- Python 3.13.3
- OpenAI API key (for API access)
- OpenAI Python SDK ≥1.0.0 (automatically installed)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/book-reader.git
   cd book-reader
   ```

2. Install the required packages using uv (recommended):
   ```
   uv pip install -e .
   ```

   Or with traditional pip:
   ```
   pip install -e .
   ```

3. Create a `.env` file in the project directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### Command Line Interface

This project provides a user-friendly command-line interface with enhanced formatting using [Rich](https://github.com/Textualize/rich).

There are several ways to run the application:

1. **As an installed command (recommended):**
   ```
   book-reader convert --sample
   ```

2. **As a Python module:**
   ```
   python -m book_reader convert --sample
   ```

3. **Using the run script:**
   ```
   python run.py convert --sample
   ```

4. **Using uv (recommended for development):**
   ```
   uv run python -m book_reader convert --sample
   ```
   This ensures the application runs within the correct virtual environment managed by uv.
   Example with options:
   ```
   uv run python -m book_reader convert --sample --max-pages 3 --voice alloy
   ```

### Using Docker

You can also run the application using the pre-built Docker image available on Docker Hub.

**Prerequisites:**
- Docker installed on your system.
- An OpenAI API Key.

**Steps:**

1.  **Pull the latest image:**
    ```bash
    docker pull juanfkurucz/book-reader:latest
    ```
    *You can replace `:latest` with a specific version tag (e.g., `:v0.1.0`) if needed.*

2.  **Building the Image Locally (Optional):**
    If you prefer to build the image yourself instead of pulling from Docker Hub:
    ```bash
    docker build -t book-reader:local .
    ```
    *This builds the image using the `Dockerfile` in the current directory and tags it as `book-reader:local`. You can then use `book-reader:local` instead of `juanfkurucz/book-reader:latest` in the `docker run` commands below.*

3.  **Prepare Directories (Create if they don't exist):**
    The container needs local directories to read PDFs from and write audiobooks to. Create them in your current terminal directory if they don't exist:
    ```bash
    # Use two separate commands for cross-platform compatibility
    mkdir books
    mkdir audiobooks
    ```
    *(You can ignore errors if the directories already exist)*

4.  **Run the container:**
    Use `docker run` to execute commands within the container. You need to:
    *   Mount your local `./books` directory to `/app/books` inside the container (`-v ./books:/app/books` on Linux/macOS or `-v ${PWD}/books:/app/books` on PowerShell or `-v %CD%\books:/app/books` on CMD).
    *   Mount your local `./audiobooks` directory to `/app/audiobooks` inside the container (`-v ./audiobooks:/app/audiobooks` on Linux/macOS or `-v ${PWD}/audiobooks:/app/audiobooks` on PowerShell or `-v %CD%\audiobooks:/app/audiobooks` on CMD).
    *   Pass your OpenAI API key as an environment variable. You have two main options:
        *   **Option A (Directly via `-e`):** Use the `-e` flag: `-e OPENAI_API_KEY="YOUR_API_KEY_HERE"`. Quick for one-off commands.
        *   **Option B (Using `--env-file`):** Create a `.env` file in your current directory with the line `OPENAI_API_KEY=YOUR_API_KEY_HERE` and use the `--env-file .env` flag. Recommended as it keeps secrets out of your command history.
    *   Specify the image name (`juanfkurucz/book-reader:latest` or your local tag like `book-reader:local`).
    *   Add the command (`list-pdfs`, `convert`) and its options.

    **Example Commands:**
    *(Using the locally built image tag `book-reader:local`. Adjust volume mounts based on your OS/shell as noted above. Examples for both `-e` and `--env-file` methods are provided below.)*

    *   **List PDFs (Linux/macOS):**
        *Using `-e`:*
        ```bash
        docker run --rm -e OPENAI_API_KEY="YOUR_API_KEY_HERE" -v ./books:/app/books -v ./audiobooks:/app/audiobooks book-reader:local list-pdfs
        ```
        *Using `--env-file`:*
        ```bash
        # Ensure .env file exists with OPENAI_API_KEY=...
        docker run --rm --env-file .env -v ./books:/app/books -v ./audiobooks:/app/audiobooks book-reader:local list-pdfs
        ```
    *   **List PDFs (Windows PowerShell):**
        *Using `-e`:*
        ```powershell
        docker run --rm -e OPENAI_API_KEY="YOUR_API_KEY_HERE" -v ${PWD}/books:/app/books -v ${PWD}/audiobooks:/app/audiobooks book-reader:local list-pdfs
        ```
        *Using `--env-file`:*
        ```powershell
        # Ensure .env file exists with OPENAI_API_KEY=...
        docker run --rm --env-file .env -v ${PWD}/books:/app/books -v ${PWD}/audiobooks:/app/audiobooks book-reader:local list-pdfs
        ```
    *   **List PDFs (Windows CMD):**
        *Using `-e`:*
        ```cmd
        docker run --rm -e OPENAI_API_KEY="YOUR_API_KEY_HERE" -v %CD%\books:/app/books -v %CD%\audiobooks:/app/audiobooks book-reader:local list-pdfs
        ```
        *Using `--env-file`:*
        ```cmd
        # Ensure .env file exists with OPENAI_API_KEY=...
        docker run --rm --env-file .env -v %CD%\books:/app/books -v %CD%\audiobooks:/app/audiobooks book-reader:local list-pdfs
        ```

    *   **Convert the sample PDF (Linux/macOS):**
        *Using `-e`:*
        ```bash
        # Ensure directories exist
        docker run --rm -e OPENAI_API_KEY="YOUR_API_KEY_HERE" -v ./books:/app/books -v ./audiobooks:/app/audiobooks book-reader:local convert --sample
        ```
        *Using `--env-file`:*
        ```bash
        # Ensure directories and .env file exist
        docker run --rm --env-file .env -v ./books:/app/books -v ./audiobooks:/app/audiobooks book-reader:local convert --sample
        ```
    *   **Convert the sample PDF (Windows PowerShell):**
        *Using `-e`:*
        ```powershell
        # Ensure directories exist
        docker run --rm -e OPENAI_API_KEY="YOUR_API_KEY_HERE" -v ${PWD}/books:/app/books -v ${PWD}/audiobooks:/app/audiobooks book-reader:local convert --sample
        ```
        *Using `--env-file`:*
        ```powershell
        # Ensure directories and .env file exist
        docker run --rm --env-file .env -v ${PWD}/books:/app/books -v ${PWD}/audiobooks:/app/audiobooks book-reader:local convert --sample
        ```
    *   **Convert the sample PDF (Windows CMD):**
        *Using `-e`:*
        ```cmd
        # Ensure directories exist
        docker run --rm -e OPENAI_API_KEY="YOUR_API_KEY_HERE" -v %CD%\books:/app/books -v %CD%\audiobooks:/app/audiobooks book-reader:local convert --sample
        ```
        *Using `--env-file`:*
        ```cmd
        # Ensure directories and .env file exist
        docker run --rm --env-file .env -v %CD%\books:/app/books -v %CD%\audiobooks:/app/audiobooks book-reader:local convert --sample
        ```

    *   **Convert a specific PDF (Linux/macOS):**
        *Using `-e`:*
        ```bash
        # Ensure mybook.pdf is in ./books
        docker run --rm -e OPENAI_API_KEY="YOUR_API_KEY_HERE" -v ./books:/app/books -v ./audiobooks:/app/audiobooks book-reader:local convert mybook.pdf --voice nova
        ```
        *Using `--env-file`:*
        ```bash
        # Ensure .env file exists and mybook.pdf is in ./books
        docker run --rm --env-file .env -v ./books:/app/books -v ./audiobooks:/app/audiobooks book-reader:local convert mybook.pdf --voice nova
        ```
    *   **Convert a specific PDF (Windows PowerShell):**
        *Using `-e`:*
        ```powershell
        # Ensure mybook.pdf is in ./books
        docker run --rm -e OPENAI_API_KEY="YOUR_API_KEY_HERE" -v ${PWD}/books:/app/books -v ${PWD}/audiobooks:/app/audiobooks book-reader:local convert mybook.pdf --voice nova
        ```
        *Using `--env-file`:*
        ```powershell
        # Ensure .env file exists and mybook.pdf is in ./books
        docker run --rm --env-file .env -v ${PWD}/books:/app/books -v ${PWD}/audiobooks:/app/audiobooks book-reader:local convert mybook.pdf --voice nova
        ```
    *   **Convert a specific PDF (Windows CMD):**
        *Using `-e`:*
        ```cmd
        # Ensure mybook.pdf is in ./books
        docker run --rm -e OPENAI_API_KEY="YOUR_API_KEY_HERE" -v %CD%\books:/app/books -v %CD%\audiobooks:/app/audiobooks book-reader:local convert mybook.pdf --voice nova
        ```
        *Using `--env-file`:*
        ```cmd
        # Ensure .env file exists and mybook.pdf is in ./books
        docker run --rm --env-file .env -v %CD%\books:/app/books -v %CD%\audiobooks:/app/audiobooks book-reader:local convert mybook.pdf --voice nova
        ```

### Available Commands

- `convert`: Convert PDF files to audiobooks
  ```
  book-reader convert [OPTIONS]
  ```

- `list-pdfs`: List all available PDF files
  ```
  book-reader list-pdfs
  ```

### Command Options

For the `convert` command:

- `--sample`: Use the sample.pdf file for testing
- `--max-pages INTEGER`: Limit the number of pages to process
- `--batch-size INTEGER`: Set the batch size for parallel processing
- `--voice TEXT`: Choose the voice to use for text-to-speech
- `--model TEXT`: Choose the TTS model to use
- `--output-dir PATH`: Directory to save the audiobook files
- `--books-dir PATH`: Directory containing PDF files
- `--resume`: Resume previous conversion

Example:
```
book-reader convert --sample --max-pages 3 --voice alloy --model tts-1-hd
```

### Available Voices

The application supports all OpenAI TTS voices including:
- `alloy`
- `ash`
- `ballad`
- `coral`
- `echo`
- `fable`
- `nova`
- `onyx`
- `sage`
- `shimmer`

### Available Models

- `tts-1`: Standard quality (lower latency)
- `tts-1-hd`: High quality (higher latency)
- `gpt-4o-mini-tts`: Newest model with the ability to follow voice instructions

## Project Structure

The application follows a modern Python package structure with clear separation of concerns:

```
book-reader/
├── src/
│   └── book_reader/        # Main package
│       ├── cli/                 # Command-line interface
│       │   ├── __init__.py
│       │   └── app.py           # CLI implementation using Click
│       ├── config/              # Application configuration
│       │   ├── __init__.py
│       │   └── settings.py      # Settings using Pydantic
│       ├── models/              # Data models
│       │   ├── __init__.py
│       │   ├── audio_config.py  # Audio configuration
│       │   └── pdf_document.py  # PDF document model
│       ├── repositories/        # Data access layer
│       │   ├── __init__.py
│       │   └── pdf_repository.py # PDF file access
│       ├── services/            # Business logic
│       │   ├── __init__.py
│       │   ├── conversion_service.py # PDF to audio conversion
│       │   └── tts_service.py   # Text-to-speech services
│       ├── utils/               # Utility functions
│       │   ├── __init__.py
│       │   ├── logging.py       # Logging utilities
│       │   └── text_processing.py # Text processing utilities
│       ├── __init__.py          # Package initialization
│       └── __main__.py          # Entry point for module execution
├── tests/                       # Test directory
│   ├── __init__.py
│   └── conftest.py              # Pytest configuration
├── books/                       # Directory for PDF files
├── audiobooks/                  # Output directory for audio files
├── run.py                       # Simple runner script
├── pyproject.toml               # Project configuration
├── setup.py                     # Setup script
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

### Architecture

The application follows a layered architecture with clear separation of concerns:

1. **CLI Layer** (`cli/`): Handles user interaction through the command line
2. **Configuration** (`config/`): Manages application settings using Pydantic
3. **Models** (`models/`): Defines data structures used throughout the application
4. **Repositories** (`repositories/`): Handles data access and storage
5. **Services** (`services/`): Implements business logic
6. **Utilities** (`utils/`): Provides helper functions and logging

This structure follows software design principles including:
- **Single Responsibility Principle**: Each module has a clear, focused purpose
- **Dependency Injection**: Services receive dependencies through constructors
- **Configuration as Code**: Settings are defined as Pydantic models

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/book-reader.git
cd book-reader

# Create a virtual environment with uv (recommended)
uv venv

# Or create a traditional virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies with uv (recommended)
uv pip install -e ".[dev]"

# Or with traditional pip
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Code Formatting and Linting

This project uses [Ruff](https://github.com/astral-sh/ruff) for code formatting and linting, and [MyPy](https://mypy.readthedocs.io/) for type checking:

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type checking
mypy src
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src
```

## Customization

You can customize the behavior in several ways:

1. **Modify the settings module**: Edit `src/book_reader/config/settings.py`
2. **Command line arguments**: Pass different options to the CLI commands
3. **Environment variables**: Set environment variables in `.env` file
4. **Extend the services**: Create custom implementations of the service classes

### Using the Library in Your Code

You can also use Book Reader as a library in your own Python projects:

```python
from pathlib import Path
from book_reader.config.settings import settings
from book_reader.models.audio_config import AudioConfig
from book_reader.models.pdf_document import PDFDocument
from book_reader.repositories.pdf_repository import PDFRepository
from book_reader.services.conversion_service import ConversionService

# Configure settings
settings.paths.books_dir = Path("./my_pdfs")
settings.paths.output_dir = Path("./my_audiobooks")
settings.audio.voice = "alloy"

# Create repository and services
repository = PDFRepository(str(settings.paths.books_dir))
service = ConversionService(repository)

# Load a PDF document
pdf_documents = repository.find_all_pdfs()
if pdf_documents:
    # Configure audio settings
    config = AudioConfig(
        model=settings.audio.model,
        voice=settings.audio.voice,
        max_text_length=settings.audio.max_text_length
    )

    # Process the document
    audio_files = service.convert_pdf_to_audiobook(
        pdf_document=pdf_documents[0],
        output_dir=settings.paths.output_dir,
        audio_config=config
    )

    print(f"Generated {len(audio_files)} audio files")
```

## Project Rules

This project follows specific development standards:

- **Python Version**: Python 3.13.3
- **Dependency Management**: uv is the designated dependency manager
- **Code Style**: Follows PEP8 guidelines
- **Design Principles**: Adheres to SOLID principles and design patterns
- **Documentation**: Comprehensive docstrings and inline comments

For more details, refer to the project's documentation and coding standards guide.

## License

This project is licensed under the terms of the included LICENSE file.

## Acknowledgements

- Uses OpenAI's API for text-to-speech conversion
- PyMuPDF for PDF processing
- Click for command-line interface
- Rich for terminal formatting
- Pydantic for configuration management

## Testing Practices

This project follows modern testing best practices to ensure code reliability and maintainability:

### Unit Testing

- Tests are designed to be fast, independent, and focused on a single responsibility
- Each component has its own test module in the `tests/` directory
- Test naming follows clear conventions that describe what is being tested
- Tests avoid implementation details and focus on behavior

### Test Organization

```
tests/
├── conftest.py           # Global test fixtures and configuration
├── models/               # Tests for data models
├── repositories/         # Tests for data access layer
├── services/             # Tests for business logic
└── utils/                # Tests for utility functions
```

### Key Testing Features

- **Parameterized Tests**: Tests for various inputs are defined once and executed with different parameters
- **Mocking**: External dependencies like OpenAI API are mocked to ensure tests are fast and deterministic
- **Fixtures**: Common test objects are managed as fixtures for reuse across tests
- **Coverage Analysis**: Test coverage is measured with pytest-cov

### Running Tests

Run the full test suite:
```bash
pytest
```

Run with coverage reporting:
```bash
pytest --cov=src/book_reader
```

Generate an HTML coverage report:
```bash
pytest --cov=src/book_reader --cov-report=html
```

Run a specific test module:
```bash
pytest tests/models/test_audio_config.py
```

Run a specific test function:
```bash
pytest tests/models/test_audio_config.py::TestAudioConfig::test_default_initialization
```
