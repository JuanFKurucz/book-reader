"""Tests for the PDF Repository."""

from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from book_reader.models.pdf_document import PDFDocument, PDFMetadata, PDFPage
from book_reader.repositories.pdf_repository import PDFRepository


@pytest.fixture
def mock_fitz_page() -> MagicMock:
    page_mock = MagicMock()
    # Define expected cleaned HTML output
    cleaned_html_output = "Page text content More text."

    # Mock get_text to return HTML or plain based on format arg
    def get_text_side_effect(format_type: str = "text") -> str:
        if format_type == "html":
            # Simulate basic HTML structure
            return f"<p>{cleaned_html_output.replace('.', '.<br/>')}</p>"
        return cleaned_html_output.replace(" ", "\n")  # Simulate plain text

    page_mock.get_text.side_effect = get_text_side_effect
    return page_mock


@pytest.fixture
def mock_fitz_document(mock_fitz_page: MagicMock) -> MagicMock:
    doc_mock = MagicMock()
    doc_mock.page_count = 2  # Set to 2 so load_pages processes 2 pages
    doc_mock.metadata = {
        "title": "Test Title",
        "author": "Test Author",
        "creationDate": "D:20230101",
        "language": "en",
    }
    doc_mock.load_page.return_value = mock_fitz_page
    # Make the mock document usable as a context manager
    doc_mock.__enter__.return_value = doc_mock
    doc_mock.__exit__.return_value = None
    return doc_mock


@pytest.fixture
def mock_fitz_open(
    mock_fitz_document: MagicMock,
) -> Generator[MagicMock, None, None]:
    # Patch fitz.open only where it's directly imported and used
    with patch(
        "book_reader.repositories.pdf_repository.fitz.open",
    ) as mock_open_ctx:
        mock_open_ctx.return_value = mock_fitz_document
        yield mock_open_ctx


@pytest.fixture
def pdf_repository(tmp_path: Path) -> PDFRepository:
    books_dir = tmp_path / "books"
    books_dir.mkdir()
    # Create dummy PDF files
    (books_dir / "test.pdf").touch()
    (books_dir / "another.pdf").touch()
    repo = PDFRepository(str(books_dir))
    return repo


@pytest.fixture
def mock_pdf_document() -> MagicMock:
    # Use MagicMock for flexibility in tests
    doc_mock = MagicMock(spec=PDFDocument)
    doc_mock.file_path = "/fake/path/document.pdf"
    doc_mock.file_name = "document.pdf"
    doc_mock.book_id = "document"
    # Create a real PDFMetadata instance for the mock
    doc_mock.metadata = PDFMetadata(
        title="Unknown Title",
        author="Unknown Author",
        date="",
        language="",
        page_count=0,
    )
    # Store pages in a list attached to the mock
    doc_mock.pages = []
    # Mock add_page to append to the list
    doc_mock.add_page.side_effect = lambda content, num: doc_mock.pages.append(
        PDFPage(content=content, page_number=num, chunks=[])
    )
    return doc_mock


class TestPDFRepository:
    """Tests for the PDFRepository class."""

    def test_init(self, tmp_path: Path) -> None:
        """Test PDFRepository initialization."""
        test_path = tmp_path / "test_init_path"
        repo = PDFRepository(str(test_path))
        assert repo.books_dir == test_path

    def test_find_all_pdfs(
        self,
        pdf_repository: PDFRepository,
    ) -> None:
        """Test finding all PDFs."""
        pdfs = pdf_repository.find_all_pdfs()
        assert len(pdfs) == 2
        assert {p.file_name for p in pdfs} == {"test.pdf", "another.pdf"}
        # Check basic properties
        assert pdfs[0].file_path.endswith(pdfs[0].file_name)
        assert pdfs[0].metadata.title == "Unknown Title"  # Metadata not loaded

    def test_find_by_filename(
        self,
        pdf_repository: PDFRepository,
    ) -> None:
        """Test finding a PDF by filename."""
        pdf = pdf_repository.find_by_filename("test.pdf")
        assert pdf is not None
        assert pdf.file_name == "test.pdf"
        assert pdf.file_path == str(pdf_repository.books_dir / "test.pdf")
        assert pdf.metadata.title == "Unknown Title"  # Metadata not loaded

    def test_find_by_filename_not_found(
        self,
        pdf_repository: PDFRepository,
    ) -> None:
        """Test finding a PDF by filename when not found."""
        pdf = pdf_repository.find_by_filename("nonexistent.pdf")
        assert pdf is None

    def test_load_pages(
        self,
        mock_fitz_open: MagicMock,
        pdf_repository: PDFRepository,
        mock_fitz_document: MagicMock,
        mock_pdf_document: MagicMock,
    ) -> None:
        """Test loading pages from a PDF."""
        # Set up mock document
        mock_fitz_document.page_count = 2  # Set to 2 to match expected calls
        # Ensure mock_fitz_document has metadata that _load_metadata can access
        mock_fitz_document.metadata = {
            "title": "Mock Title",
            "author": "Mock Author",
        }

        # Create a fresh PDFMetadata for the mock document
        mock_pdf_document.metadata = PDFMetadata(
            title="Unknown Title",
            author="Unknown Author",
            date="",
            language="",
            page_count=0,
        )

        # Call the method under test
        pdf_document = pdf_repository.load_pages(
            mock_pdf_document,
            max_pages=2,
        )
        assert pdf_document.pages  # Verify pages were loaded
        assert len(pdf_document.pages) <= 2  # Verify max_pages was applied

        # Verify fitz.open was called
        mock_fitz_open.assert_called_once_with(mock_pdf_document.file_path)

        # Verify pages were added (should be called exactly twice)
        assert mock_pdf_document.add_page.call_count == 2
        # Verify first call was for page 0
        mock_pdf_document.add_page.assert_any_call(
            "Page text content More text.",
            0,
        )
        # Verify second call was for page 1
        mock_pdf_document.add_page.assert_any_call(
            "Page text content More text.",
            1,
        )

        # Verify metadata was loaded
        assert mock_pdf_document.metadata.title == "Mock Title"
        assert mock_pdf_document.metadata.author == "Mock Author"
        assert mock_pdf_document.metadata.page_count == 2

    def test_extract_text_from_page_internal(
        self,
        pdf_repository: PDFRepository,
        mock_fitz_document: MagicMock,
        mock_fitz_page: MagicMock,
    ) -> None:
        """Test the internal _extract_text_from_page method."""
        # Set up the mock document to return our mock page
        mock_fitz_document.load_page.return_value = mock_fitz_page

        # Call the method under test directly with the mock document
        text = pdf_repository._extract_text_from_page(mock_fitz_document, 0)

        # Verify the text was extracted correctly
        assert text == "Page text content More text."
        # Verify get_text was called with the HTML format
        mock_fitz_page.get_text.assert_called_once_with("html")

    def test_clean_text(self) -> None:
        cleaned = PDFRepository._clean_text("  Line 1 \n\n Line 2  \n")
        assert cleaned == "Line 1\nLine 2"
