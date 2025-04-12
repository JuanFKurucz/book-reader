"""PDF Document model."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class PDFMetadata:
    """PDF Metadata model."""

    title: str = "Unknown Title"
    author: str = "Unknown Author"
    date: str = "Unknown Date"
    language: str = "Unknown Language"
    page_count: int = 0

    @classmethod
    def create_empty(cls) -> "PDFMetadata":
        """Create an empty metadata object."""
        return cls()


@dataclass
class PDFPage:
    """PDF Page model."""

    content: str
    page_number: int
    chunks: List[str] = field(default_factory=list)


@dataclass
class PDFDocument:
    """PDF Document model."""

    file_path: str
    file_name: str
    metadata: PDFMetadata = field(default_factory=PDFMetadata.create_empty)
    pages: List[PDFPage] = field(default_factory=list)

    @property
    def book_id(self) -> str:
        """Get the unique book ID based on the file name without extension."""
        return self.file_name.rsplit(".", 1)[0]

    def add_page(self, content: str, page_number: int) -> None:
        """Add a page to the document."""
        self.pages.append(PDFPage(content=content, page_number=page_number))
