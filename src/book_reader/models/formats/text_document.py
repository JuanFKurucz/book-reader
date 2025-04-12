"""Text Document model."""

from dataclasses import dataclass

from book_reader.models.base.document import BaseDocument


@dataclass
class TextDocument(BaseDocument):
    """Text Document model for plain text files."""

    format: str = "txt"
