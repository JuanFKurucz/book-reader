"""EPUB Repository for handling EPUB files."""

from typing import List, Optional, cast

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub
from loguru import logger

from book_reader.models.base.document import BaseDocument
from book_reader.models.formats.epub_document import EPUBDocument
from book_reader.repositories.base.base_repository import BaseRepository


class EPUBRepository(BaseRepository[EPUBDocument]):
    """Repository for accessing and managing EPUB documents."""

    def find_all_documents(self) -> List[EPUBDocument]:
        """Find all EPUB documents in the books directory."""
        if not self.books_dir.is_dir():
            return []

        epub_documents: List[EPUBDocument] = []
        for epub_path in self.books_dir.glob("*.epub"):
            try:
                # Only create the object, don't load metadata/pages here
                doc = EPUBDocument(
                    file_path=str(epub_path),
                    file_name=epub_path.name,
                )
                epub_documents.append(doc)
            except Exception as e:
                err_msg = f"Error loading metadata for {epub_path}: {e}"
                logger.error(err_msg)
        return epub_documents

    def find_by_filename(self, filename: str) -> Optional[EPUBDocument]:
        """Find an EPUB document by its filename."""
        epub_path = self.books_dir / filename
        if epub_path.is_file() and epub_path.suffix.lower() == ".epub":
            try:
                # Only create the object
                return EPUBDocument(
                    file_path=str(epub_path),
                    file_name=filename,
                )
            except Exception as e:
                err_msg = f"Error loading metadata for {epub_path}: {e}"
                logger.error(err_msg)
                return None
        return None

    def load_pages(
        self,
        document: BaseDocument,
        max_pages: Optional[int] = None,
    ) -> EPUBDocument:
        """Load pages from the EPUB document.

        Args:
            document: The EPUB document to load pages from.
            max_pages: Maximum number of pages to load. If None, all pages.

        Returns:
            The EPUB document with pages loaded.
        """
        # Type check and cast
        if not isinstance(document, EPUBDocument):
            raise TypeError("Expected EPUBDocument instance")

        epub_document = cast(EPUBDocument, document)

        try:
            # Load the EPUB file
            book = epub.read_epub(epub_document.file_path)

            # Load metadata
            self._load_metadata(epub_document, book)

            # Get all HTML items (chapters)
            chapters = [
                item
                for item in book.get_items()
                if item.get_type() == ebooklib.ITEM_DOCUMENT
            ]

            # Determine how many chapters to process
            num_chapters_to_load = (
                min(max_pages, len(chapters)) if max_pages else len(chapters)
            )

            # Process each chapter
            for chapter_num in range(num_chapters_to_load):
                chapter = chapters[chapter_num]
                content = chapter.get_content().decode("utf-8")
                text = self._extract_text_from_html(content)
                epub_document.add_page(text, chapter_num)

        except Exception as e:
            msg = f"Error loading pages for {epub_document.file_name}: {e}"
            logger.error(msg)

        return epub_document

    def _load_metadata(
        self,
        document: EPUBDocument,
        book: epub.EpubBook,
    ) -> None:
        """Load metadata from the EPUB document."""
        try:
            # Get title
            title = book.get_metadata("DC", "title")
            if title:
                document.metadata.title = title[0][0]

            # Get author
            creator = book.get_metadata("DC", "creator")
            if creator:
                document.metadata.author = creator[0][0]

            # Get language
            language = book.get_metadata("DC", "language")
            if language:
                document.metadata.language = language[0][0]

            # Get date
            date = book.get_metadata("DC", "date")
            if date:
                document.metadata.date = date[0][0]

            # Get page count (approximate by chapter count)
            document.metadata.page_count = len(
                [
                    item
                    for item in book.get_items()
                    if item.get_type() == ebooklib.ITEM_DOCUMENT
                ]
            )

        except Exception as e:
            msg = f"Error loading metadata for {document.file_name}: {e}"
            logger.error(msg)

    def _extract_text_from_html(self, html_content: str) -> str:
        """Extract clean text from HTML content."""
        try:
            soup = BeautifulSoup(html_content, "html.parser")

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()

            # Get text
            text = soup.get_text()

            # Clean the text
            return self._clean_text(text)

        except Exception as e:
            logger.error(f"Error extracting text from HTML: {e}")
            return ""

    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean the text by removing extra whitespace and empty lines.

        Args:
            text: Raw text from HTML

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
        return [".epub"]
