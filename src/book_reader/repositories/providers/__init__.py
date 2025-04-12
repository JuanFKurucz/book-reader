"""Repository provider implementations package."""

from book_reader.repositories.providers.epub_repository import EPUBRepository
from book_reader.repositories.providers.pdf_repository import PDFRepository
from book_reader.repositories.providers.text_repository import TextRepository

__all__ = ["PDFRepository", "EPUBRepository", "TextRepository"]
