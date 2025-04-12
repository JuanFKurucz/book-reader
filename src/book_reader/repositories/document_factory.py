"""Document Factory for creating repositories based on file extension."""

import os
from typing import Dict, List, Optional, Type

from loguru import logger

from book_reader.repositories.base.base_repository import BaseRepository
from book_reader.repositories.providers.epub_repository import EPUBRepository
from book_reader.repositories.providers.pdf_repository import PDFRepository
from book_reader.repositories.providers.text_repository import TextRepository


class DocumentFactory:
    """Factory for creating document repositories based on file extension."""

    # Mapping of file extensions to repository classes
    _repository_classes: Dict[str, Type[BaseRepository]] = {
        ".pdf": PDFRepository,
        ".epub": EPUBRepository,
        ".txt": TextRepository,
    }

    @classmethod
    def get_repository_for_file(
        cls, file_path: str, books_dir: str
    ) -> Optional[BaseRepository]:
        """Get an appropriate repository for the given file.

        Args:
            file_path: Path to the file
            books_dir: Directory containing book files

        Returns:
            Repository instance or None if no appropriate repository is found
        """
        _, ext = os.path.splitext(file_path.lower())
        repo_class = cls._repository_classes.get(ext)

        if repo_class:
            return repo_class(books_dir)

        logger.warning(f"No repository found for file type: {ext}")
        return None

    @classmethod
    def get_repository_for_extension(
        cls, extension: str, books_dir: str
    ) -> Optional[BaseRepository]:
        """Get an appropriate repository for the given file extension.

        Args:
            extension: File extension (e.g., ".pdf", ".epub")
            books_dir: Directory containing book files

        Returns:
            Repository instance or None if no appropriate repository is found
        """
        # Ensure the extension starts with a dot
        if not extension.startswith("."):
            extension = f".{extension}"

        repo_class = cls._repository_classes.get(extension.lower())

        if repo_class:
            return repo_class(books_dir)

        logger.warning(f"No repository found for file type: {extension}")
        return None

    @classmethod
    def get_all_repositories(cls, books_dir: str) -> List[BaseRepository]:
        """Get instances of all available repositories.

        Args:
            books_dir: Directory containing book files

        Returns:
            List of all repository instances
        """
        repositories = []

        for repo_class in set(cls._repository_classes.values()):
            repositories.append(repo_class(books_dir))

        return repositories

    @classmethod
    def get_supported_extensions(cls) -> List[str]:
        """Get all supported file extensions.

        Returns:
            List of all supported file extensions
        """
        return list(cls._repository_classes.keys())
