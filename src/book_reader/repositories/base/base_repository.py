"""Base repository module."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, List, Optional, TypeVar

from book_reader.models.base.document import BaseDocument

# Generic type for document implementations
T_co = TypeVar("T_co", bound=BaseDocument, covariant=True)


class BaseRepository(Generic[T_co], ABC):
    """Base repository interface for document repositories."""

    def __init__(self, books_dir: str) -> None:
        """Initialize the repository.

        Args:
            books_dir: Path to the directory containing document files.
        """
        self.books_dir = Path(books_dir)
        if not self.books_dir.is_dir():
            self.books_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def find_all_documents(self) -> List[T_co]:
        """Find all documents of the supported type in the books directory.

        Returns:
            List of document objects.
        """
        pass

    @abstractmethod
    def find_by_filename(self, filename: str) -> Optional[T_co]:
        """Find a document by its filename.

        Args:
            filename: The filename to search for.

        Returns:
            Document object if found, None otherwise.
        """
        pass

    @abstractmethod
    def load_pages(
        self,
        document: BaseDocument,  # Use BaseDocument instead of T
        max_pages: Optional[int] = None,
    ) -> T_co:
        """Load pages from the document.

        Args:
            document: The document to load pages from.
            max_pages: Maximum number of pages to load. If None, all pages.

        Returns:
            The document with pages loaded.
        """
        pass

    @property
    @abstractmethod
    def supported_extensions(self) -> List[str]:
        """Get the list of file extensions supported by this repository.

        Returns:
            List of supported file extensions (e.g., [".pdf", ".epub"]).
        """
        pass
