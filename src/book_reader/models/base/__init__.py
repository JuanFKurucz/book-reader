"""Base models package."""

from book_reader.models.base.document import (
    BaseDocument,
    DocumentMetadata,
    DocumentPage,
)

__all__ = ["BaseDocument", "DocumentMetadata", "DocumentPage"]
