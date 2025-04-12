"""EPUB Document model."""

from dataclasses import dataclass

from book_reader.models.base.document import BaseDocument


@dataclass
class EPUBDocument(BaseDocument):
    """EPUB Document model for e-books in EPUB format."""

    format: str = "epub"
