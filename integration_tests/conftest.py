"""Fixtures for integration tests."""

import os
import shutil
from pathlib import Path
from typing import Generator, List, Tuple

import pytest

# Define sample documents for each format
PDF_SAMPLE = "sample.pdf"
EPUB_SAMPLE = "sample.epub"
TEXT_SAMPLE = "sample.txt"


@pytest.fixture
def temp_output_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary directory for test output files."""
    output_dir = tmp_path / "output"
    output_dir.mkdir(exist_ok=True)
    yield output_dir
    # Clean up output files after test
    if output_dir.exists():
        shutil.rmtree(output_dir)


@pytest.fixture
def temp_books_dir(
    tmp_path: Path,
) -> Generator[Tuple[Path, List[str]], None, None]:
    """Create a temporary directory with sample books for testing."""
    books_dir = tmp_path / "books"
    books_dir.mkdir(exist_ok=True)

    # Copy sample files from the real books directory to the temp directory
    source_dir = Path("books")

    # Ensure we have all needed sample files
    samples = []
    if (source_dir / PDF_SAMPLE).exists():
        shutil.copy(source_dir / PDF_SAMPLE, books_dir / PDF_SAMPLE)
        samples.append(PDF_SAMPLE)

    # Yield the directory and the list of available samples
    yield books_dir, samples

    # Clean up after test
    if books_dir.exists():
        shutil.rmtree(books_dir)


@pytest.fixture
def check_api_key() -> None:
    """Check if OpenAI API key is available."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY environment variable not set")
