"""Repositories package for PDF to Audiobook Converter."""

# Base repositories
from book_reader.repositories.base.base_repository import BaseRepository

# Factory
from book_reader.repositories.document_factory import DocumentFactory
from book_reader.repositories.providers.epub_repository import EPUBRepository

# Provider repositories
from book_reader.repositories.providers.pdf_repository import PDFRepository
from book_reader.repositories.providers.text_repository import TextRepository

__all__ = [
    # Base
    "BaseRepository",
    # Providers
    "PDFRepository",
    "EPUBRepository",
    "TextRepository",
    # Factory
    "DocumentFactory",
]
