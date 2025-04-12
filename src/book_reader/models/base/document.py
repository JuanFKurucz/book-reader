"""Base Document models."""

from abc import ABC
from dataclasses import dataclass, field
from typing import List


@dataclass
class DocumentMetadata:
    """Base metadata model for all document types."""

    title: str = "Unknown Title"
    author: str = "Unknown Author"
    date: str = "Unknown Date"
    language: str = "Unknown Language"
    page_count: int = 0

    @classmethod
    def create_empty(cls) -> "DocumentMetadata":
        """Create an empty metadata object."""
        return cls()


@dataclass
class DocumentPage:
    """Base page model for all document types."""

    content: str
    page_number: int
    chunks: List[str] = field(default_factory=list)


@dataclass
class BaseDocument(ABC):
    """Base document model that all format-specific models will inherit from."""

    file_path: str
    file_name: str
    metadata: DocumentMetadata = field(default_factory=DocumentMetadata.create_empty)
    pages: List[DocumentPage] = field(default_factory=list)
    # The file format (pdf, epub, txt, etc.)
    format: str = "unknown"

    @property
    def book_id(self) -> str:
        """Get the unique book ID based on the file name without extension."""
        return self.file_name.rsplit(".", 1)[0]

    def add_page(self, content: str, page_number: int) -> None:
        """Add a page to the document."""
        self.pages.append(DocumentPage(content=content, page_number=page_number))

    @property
    def extension(self) -> str:
        """Get the file extension."""
        if "." in self.file_name:
            return self.file_name.rsplit(".", 1)[1].lower()
        return ""
