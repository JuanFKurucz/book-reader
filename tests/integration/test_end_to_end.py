"""End-to-end integration tests."""

from pathlib import Path
from typing import List, Tuple

import pytest
from click.exceptions import Exit

from book_reader.cli.app import cli
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
        msg = f"Sample PDF file ({PDF_SAMPLE}) not found in books directory"
        pytest.skip(msg)

    # Execute the command (with minimal content since we're testing)
    args = [
        "convert",
        PDF_SAMPLE,
        "--max-pages",
        "1",
        "--books-dir",
        str(books_dir),
        "--output-dir",
        str(temp_output_dir),
    ]

    # Run the command and expect a clean exit
    try:
        cli(args)
    except (Exit, SystemExit) as e:
        # Handle both Click's Exit and SystemExit
        if isinstance(e, SystemExit):
            assert e.code == 0
        else:
            # Click's Exit doesn't have a code attribute
            pass

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

    # Execute the command
    args = [
        "convert",
        TEXT_SAMPLE,
        "--books-dir",
        str(books_dir),
        "--output-dir",
        str(temp_output_dir),
    ]

    # Run the command and expect a clean exit
    try:
        cli(args)
    except (Exit, SystemExit) as e:
        # Handle both Click's Exit and SystemExit
        if isinstance(e, SystemExit):
            assert e.code == 0
        else:
            # Click's Exit doesn't have a code attribute
            pass

    # Check if output files were created
    output_files = list(temp_output_dir.glob("**/*.mp3"))
    assert len(output_files) > 0, "No output audio files were created"

    # Check if the output files have content
    for output_file in output_files:
        file_size = output_file.stat().st_size
        assert file_size > 0, f"Output file {output_file} is empty"
