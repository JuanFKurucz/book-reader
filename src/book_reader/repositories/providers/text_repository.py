"""Text Repository for handling text files."""

from typing import List, Optional, cast

from loguru import logger

from book_reader.models.base.document import BaseDocument
from book_reader.models.formats.text_document import TextDocument
from book_reader.repositories.base.base_repository import BaseRepository


class TextRepository(BaseRepository[TextDocument]):
    """Repository for accessing and managing plain text documents."""

    def find_all_documents(self) -> List[TextDocument]:
        """Find all text documents in the books directory."""
        if not self.books_dir.is_dir():
            return []

        text_documents: List[TextDocument] = []
        for text_path in self.books_dir.glob("*.txt"):
            try:
                # Only create the object, don't load content here
                doc = TextDocument(
                    file_path=str(text_path),
                    file_name=text_path.name,
                )
                text_documents.append(doc)
            except Exception as e:
                err_msg = f"Error loading text file {text_path}: {e}"
                logger.error(err_msg)
        return text_documents

    def find_by_filename(self, filename: str) -> Optional[TextDocument]:
        """Find a text document by its filename."""
        text_path = self.books_dir / filename
        if text_path.is_file() and text_path.suffix.lower() == ".txt":
            try:
                # Only create the object
                return TextDocument(
                    file_path=str(text_path),
                    file_name=filename,
                )
            except Exception as e:
                err_msg = f"Error loading text file {text_path}: {e}"
                logger.error(err_msg)
                return None
        return None

    def load_pages(
        self,
        document: BaseDocument,
        max_pages: Optional[int] = None,
    ) -> TextDocument:
        """Load content from the text document.

        For text files, the entire content is treated as a single page.
        The max_pages parameter is ignored for text files.

        Args:
            document: The text document to load content from.
            max_pages: Ignored for text files.

        Returns:
            The text document with content loaded.
        """
        # Type check and cast
        if not isinstance(document, TextDocument):
            raise TypeError("Expected TextDocument instance")

        text_document = cast(TextDocument, document)

        try:
            # Set basic metadata
            self._set_basic_metadata(text_document)

            # Read the text file
            with open(text_document.file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Clean the text
            clean_content = self._clean_text(content)

            # Add as a single page
            text_document.add_page(clean_content, 0)

        except Exception as e:
            msg = f"Error loading content for {text_document.file_name}: {e}"
            logger.error(msg)

        return text_document

    def _set_basic_metadata(self, document: TextDocument) -> None:
        """Set basic metadata for the text document.

        Uses the filename as the title and other defaults.

        Args:
            document: The text document to set metadata for.
        """
        try:
            # Use filename without extension as title
            document.metadata.title = document.book_id

            # Set defaults for other metadata
            document.metadata.author = "Unknown Author"
            document.metadata.date = ""
            document.metadata.language = "Unknown Language"
            document.metadata.page_count = 1  # Text files are treated as one page

        except Exception as e:
            msg = f"Error setting metadata for {document.file_name}: {e}"
            logger.error(msg)

    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean the text by removing extra whitespace and empty lines.

        Args:
            text: Raw text from the file

        Returns:
            Cleaned text
        """
        lines = text.split("\n")
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        cleaned_text = "\n".join(cleaned_lines)
        return cleaned_text

    @property
    def supported_extensions(self) -> List[str]:
        """Get the list of file extensions supported by this repository."""
        return [".txt"]
