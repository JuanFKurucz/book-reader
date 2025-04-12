"""Pytest configuration for PDF to Audiobook tests."""

import os

# Ensure tests can find the package
import sys
from pathlib import Path

import pytest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)


@pytest.fixture
def test_dir() -> Path:
    """Return the path to the tests directory."""
    return Path(__file__).parent


@pytest.fixture
def sample_pdf_path(test_dir: Path) -> Path:
    """Return the path to a sample PDF file for testing."""
    samples_dir = test_dir / "samples"
    samples_dir.mkdir(exist_ok=True)
    sample_path = samples_dir / "sample.pdf"

    # Create a dummy PDF file if it doesn't exist
    if not sample_path.exists():
        try:
            import fitz  # PyMuPDF

            doc = fitz.open()  # Create a new empty PDF
            page = doc.new_page()  # Add a new page
            text = "This is a test PDF document for PDF to Audiobook converter."
            page.insert_text((50, 50), text)
            doc.save(str(sample_path))
            doc.close()
        except ImportError:
            # Fallback - create an empty file if PyMuPDF is not available
            with open(sample_path, "wb") as f:
                f.write(
                    b"%PDF-1.7\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
                    b"trailer\n<< /Root 1 0 R >>\n%%EOF"
                )

    return sample_path


@pytest.fixture
def temp_output_dir(tmp_path: Path) -> Path:
    """Create a temporary directory for test output files."""
    output_dir = tmp_path / "audiobooks"
    output_dir.mkdir(exist_ok=True)
    return output_dir
