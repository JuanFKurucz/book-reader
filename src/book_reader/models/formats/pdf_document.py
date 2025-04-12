"""PDF Document model."""

from dataclasses import dataclass, field
from typing import List

from book_reader.models.base.document import (
    BaseDocument,
    DocumentMetadata,
    DocumentPage,
)


@dataclass
class PDFMetadata(DocumentMetadata):
    """PDF Metadata model."""

    # Inherits all fields from DocumentMetadata
    # No need to override defaults unless we want PDF-specific changes

    @classmethod
    def create_empty(cls) -> "PDFMetadata":
        """Create an empty metadata object."""
        return cls()


@dataclass
class PDFPage(DocumentPage):
    """PDF Page model."""

    # Inherits all fields from DocumentPage
    # No need to redefine fields


@dataclass
class PDFDocument(BaseDocument):
    """PDF Document model."""

    format: str = "pdf"  # Override the format field
    # These are inherited from BaseDocument, just explicitly listed for clarity
    file_path: str = field(default="")
    file_name: str = field(default="")
    # Now properly using inheritance
    metadata: DocumentMetadata = field(default_factory=PDFMetadata.create_empty)
    pages: List[DocumentPage] = field(default_factory=list)

    @property
    def book_id(self) -> str:
        """Get the unique book ID based on the file name without extension."""
        return self.file_name.rsplit(".", 1)[0]

    def add_page(self, content: str, page_number: int) -> None:
        """Add a page to the document."""
        self.pages.append(PDFPage(content=content, page_number=page_number))
