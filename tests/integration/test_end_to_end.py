"""End-to-end integration tests for Book Reader."""

import os
import subprocess
from pathlib import Path
from typing import List, Tuple

import pytest

from tests.integration.conftest import PDF_SAMPLE, TEXT_SAMPLE


# Mark this test as expensive to ensure it's skipped by default
@pytest.mark.expensive
def test_pdf_conversion(
    temp_output_dir: Path,
    temp_books_dir: Tuple[Path, List[str]],
    check_api_key: None,
) -> None:
    """Test end-to-end PDF conversion."""
    books_dir, samples = temp_books_dir

    # Skip if sample PDF not available
    if PDF_SAMPLE not in samples:
        pytest.skip(f"Sample PDF file ({PDF_SAMPLE}) not found in books directory")

    # Execute the command (with minimal content since we're testing)
    cmd = [
        "python",
        "-m",
        "book_reader.cli.app",
        "convert",
        PDF_SAMPLE,
        "--max-pages",
        "1",
        "--books-dir",
        str(books_dir),
        "--output-dir",
        str(temp_output_dir),
    ]

    # Run the command and check output
    result = subprocess.run(cmd, capture_output=True, text=True, env={**os.environ})

    # Check if the command succeeded
    assert result.returncode == 0, f"Command failed: {result.stderr}"

    # Check if output files were created
    output_files = list(temp_output_dir.glob("**/*.mp3"))
    assert len(output_files) > 0, "No output audio files were created"

    # Check if the output files have content
    for output_file in output_files:
        file_size = output_file.stat().st_size
        assert file_size > 0, f"Output file {output_file} is empty"


# Mark this test as expensive to ensure it's skipped by default
@pytest.mark.expensive
def test_text_conversion(
    temp_output_dir: Path,
    temp_books_dir: Tuple[Path, List[str]],
    check_api_key: None,
) -> None:
    """Test end-to-end text file conversion."""
    books_dir, samples = temp_books_dir

    # Create the text sample if it doesn't exist
    if TEXT_SAMPLE not in samples:
        # Create sample text
        sample_path = books_dir / TEXT_SAMPLE
        with open(sample_path, "w") as f:
            f.write("# Sample Text Document\n\n")
            f.write("This is a sample text for testing TTS conversion.\n")
            f.write("It is kept very brief to minimize API usage.")

        # Note: in a real test we'd create a more substantial document
        # but for this example we're keeping it minimal

    # Execute the command
    cmd = [
        "python",
        "-m",
        "book_reader.cli.app",
        "convert",
        TEXT_SAMPLE,
        "--books-dir",
        str(books_dir),
        "--output-dir",
        str(temp_output_dir),
    ]

    # Run the command and check output
    result = subprocess.run(cmd, capture_output=True, text=True, env={**os.environ})

    # Check if the command succeeded
    assert result.returncode == 0, f"Command failed: {result.stderr}"

    # Check if output files were created
    output_files = list(temp_output_dir.glob("**/*.mp3"))
    assert len(output_files) > 0, "No output audio files were created"

    # Check if the output files have content
    for output_file in output_files:
        file_size = output_file.stat().st_size
        assert file_size > 0, f"Output file {output_file} is empty"
