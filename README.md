# Book Reader

A modern, well-structured Python tool that converts PDF files to audiobooks using OpenAI's Text-to-Speech API.

[![Documentation Status](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://juanfkurucz.github.io/book-reader/)
[![Python Version](https://img.shields.io/badge/python-3.13.3-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Book Reader is a command-line utility designed to transform PDF documents into high-quality audiobooks using OpenAI's Text-to-Speech API. The tool handles text extraction, processing, and audio generation with an emphasis on usability, performance, and reliability.

📚 → 🔊 PDF to Audiobook conversion made simple!

## Key Features

- Extract text from PDF files
- Convert text to high-quality audio using OpenAI's TTS API
- Process PDFs in batches with parallel execution
- Resume interrupted conversions
- Support for all OpenAI TTS voices and models
- User-friendly command-line interface with rich formatting
- Docker support for easy deployment

## Quick Start

### Installation

```bash
# Install from PyPI
pip install book-reader

# Or with uv (recommended)
uv pip install book-reader
```

### Basic Usage

```bash
# Convert a PDF with default settings
book-reader convert path/to/your/document.pdf

# Try the sample PDF with a specific voice
book-reader convert --sample --voice nova

# Get help
book-reader --help
```

### Docker

```bash
# Pull the Docker image
docker pull juanfkurucz/book-reader:latest

# Run with your PDF files mounted
docker run --rm \
  -v ./books:/app/books \
  -v ./audiobooks:/app/audiobooks \
  -e OPENAI_API_KEY="your-api-key-here" \
  juanfkurucz/book-reader:latest \
  convert --sample
```

## Documentation

For complete documentation, visit:

📖 **[Book Reader Documentation](https://juanfkurucz.github.io/book-reader/)**

The documentation includes:
- [Installation Guide](https://juanfkurucz.github.io/book-reader/installation/)
- [Usage Guide](https://juanfkurucz.github.io/book-reader/usage/)
- [Configuration Guide](https://juanfkurucz.github.io/book-reader/configuration/)
- [API Reference](https://juanfkurucz.github.io/book-reader/api/)
- [Contributing Guide](https://juanfkurucz.github.io/book-reader/contributing/)

## Requirements

- Python 3.13.3 or higher
- OpenAI API key with access to the TTS API

## Project Structure

Book Reader follows a modern Python package structure with clear separation of concerns:

```
book-reader/
├── src/                # Source code
├── docs/               # Documentation
├── tests/              # Test suite
│   └── integration/    # End-to-end tests with real API calls
└── ...                 # Configuration files
```

For more details about the architecture and components, see the [API documentation](https://juanfkurucz.github.io/book-reader/api/).

## Testing

Book Reader includes both unit tests and integration tests:

### Unit Tests

Run the unit tests with:

```bash
# Using pytest directly
pytest

# Or with uv
uv run pytest
```

### Integration Tests

The project includes end-to-end integration tests that perform real API calls to OpenAI. These tests:
- Require an OpenAI API key (from environment variable or .env file)
- Consume API credits
- Are skipped by default in normal test runs

To run integration tests:

```bash
# Set your OpenAI API key (if not in .env file)
export OPENAI_API_KEY=your-api-key

# Run all integration tests using uv
uv run pytest tests/integration/

# Run specific integration test file
uv run pytest tests/integration/test_end_to_end.py

# Run integration tests with sample generation
uv run pytest tests/integration/create_samples.py

# Run with verbose output
uv run pytest -v tests/integration/

# Run with coverage report
uv run pytest --cov=book_reader tests/integration/
```

Note: Integration tests may take longer to run as they interact with external services. Make sure you have sufficient API credits before running them.

For more details, see [Integration Tests README](tests/integration/README.md).

## Acknowledgements

Book Reader was inspired by and built upon the valuable work of the following projects and developers:

- [epub-to-audiobook](https://github.com/fairy-root/epub-to-audiobook) by [fairy-root](https://github.com/fairy-root)
- [bulletReader](https://github.com/facundop3/bulletReader) by [facundop3](https://github.com/facundop3)

## Contributing

Contributions are welcome! Please see our [Contributing Guide](https://juanfkurucz.github.io/book-reader/contributing/) for details on how to get started.

## License

This project is licensed under the terms of the MIT License.
