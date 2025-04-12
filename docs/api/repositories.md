# Repositories

This page documents the repository classes used in Book Reader for data access.

## PDFRepository

The `PDFRepository` class is responsible for finding, loading, and extracting text from PDF documents.

```python
class PDFRepository:
    """Repository for PDF document operations."""

    def find_all_pdfs(self, directory: str) -> List[PDFDocument]:
        """Find all PDF files in the specified directory.

        Args:
            directory: Directory path to search for PDFs

        Returns:
            List of PDFDocument objects
        """

    def find_by_filename(self, filename: str) -> PDFDocument:
        """Find a PDF document by its filename.

        Args:
            filename: Path to the PDF file

        Returns:
            PDFDocument object

        Raises:
            FileNotFoundError: If the file doesn't exist or isn't a PDF
        """

    def load_pages(self, document: PDFDocument, page_range: Optional[Tuple[int, int]] = None) -> List[PDFPage]:
        """Load pages from a PDF document.

        Args:
            document: PDFDocument to load pages from
            page_range: Optional tuple of (start_page, end_page) to load a subset of pages

        Returns:
            List of PDFPage objects

        Raises:
            PDFReadError: If there's an error reading the PDF
        """
```

## AudioRepository

The `AudioRepository` class handles storage and retrieval of audio files.

```python
class AudioRepository:
    """Repository for audio file operations."""

    def save_audio(self, audio_data: bytes, output_path: str) -> None:
        """Save audio data to a file.

        Args:
            audio_data: The binary audio data
            output_path: Path where the audio file should be saved

        Raises:
            IOError: If there's an error writing the file
        """

    def get_audio_duration(self, file_path: str) -> float:
        """Get the duration of an audio file in seconds.

        Args:
            file_path: Path to the audio file

        Returns:
            Duration in seconds

        Raises:
            IOError: If there's an error reading the file
        """
```

## ProgressRepository

The `ProgressRepository` class handles saving and loading conversion progress.

```python
class ProgressRepository:
    """Repository for managing conversion progress."""

    def save_progress(self, conversion_id: str, status: ConversionStatus) -> None:
        """Save the current progress of a conversion.

        Args:
            conversion_id: Unique identifier for the conversion
            status: Current status of the conversion
        """

    def load_progress(self, conversion_id: str) -> Optional[ConversionStatus]:
        """Load the progress of a conversion.

        Args:
            conversion_id: Unique identifier for the conversion

        Returns:
            ConversionStatus object if progress exists, None otherwise
        """
```

## Base Interfaces

Book Reader uses interfaces (abstract base classes) to define the contract for repositories:

```python
class BasePDFRepository(ABC):
    """Base interface for PDF repositories."""

    @abstractmethod
    def find_by_filename(self, filename: str) -> PDFDocument:
        """Find a PDF document by its filename."""
        pass

    @abstractmethod
    def load_pages(self, document: PDFDocument, page_range: Optional[Tuple[int, int]] = None) -> List[PDFPage]:
        """Load pages from a PDF document."""
        pass
```

For complete implementation details of these repositories, please refer to the source code.
