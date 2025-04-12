# Services

This page documents the service classes used in Book Reader for business logic operations.

## ConversionService

The `ConversionService` is the main service that handles the conversion of PDF documents to audiobooks.

```python
class ConversionService:
    """Service for converting PDF documents to audiobooks."""

    def __init__(
        self,
        openai_api_key: str,
        pdf_repository: BasePDFRepository,
        tts_service: Optional[BaseTTSService] = None
    ):
        """Initialize the conversion service.

        Args:
            openai_api_key: OpenAI API key for TTS
            pdf_repository: Repository for PDF operations
            tts_service: Optional TTS service (will be created if not provided)
        """

    def convert_pdf_to_audiobook(
        self,
        pdf_document: PDFDocument,
        output_dir: str,
        audio_config: AudioConfig,
        batch_size: int = 15,
        resume: bool = False,
        max_pages: Optional[int] = None
    ) -> ConversionResult:
        """Convert a PDF document to audiobook.

        Args:
            pdf_document: The PDF document to convert
            output_dir: Directory to save the audio files
            audio_config: Configuration for the audio conversion
            batch_size: Number of pages to process in a batch
            resume: Whether to resume a previous conversion
            max_pages: Maximum number of pages to process

        Returns:
            ConversionResult containing details about the conversion

        Raises:
            PDFReadError: If there's an error reading the PDF
            TTSError: If there's an error with the TTS service
            IOError: If there's an error writing the audio files
        """
```

## TTSService

The `TTSService` interfaces with OpenAI's Text-to-Speech API.

```python
class TTSService:
    """Service for text-to-speech conversion using OpenAI's API."""

    def __init__(self, api_key: str):
        """Initialize the TTS service.

        Args:
            api_key: OpenAI API key
        """

    def convert_text_to_speech(
        self,
        text: str,
        audio_config: AudioConfig,
        output_path: Optional[str] = None
    ) -> bytes:
        """Convert text to speech.

        Args:
            text: The text to convert to speech
            audio_config: Configuration for the audio conversion
            output_path: Optional path to save the audio file

        Returns:
            Binary audio data

        Raises:
            TTSError: If there's an error with the TTS service
            IOError: If there's an error writing the audio file
        """
```

## TextProcessingService

The `TextProcessingService` handles text preprocessing before sending it to the TTS service.

```python
class TextProcessingService:
    """Service for text preprocessing and optimization."""

    def preprocess_text(self, text: str) -> str:
        """Preprocess text for optimal TTS conversion.

        Args:
            text: The text to preprocess

        Returns:
            Preprocessed text
        """

    def split_into_chunks(
        self,
        pages: List[PDFPage],
        max_chunk_size: int = 4000
    ) -> List[TextChunk]:
        """Split pages into manageable text chunks.

        Args:
            pages: List of PDF pages
            max_chunk_size: Maximum size of each chunk in characters

        Returns:
            List of TextChunk objects
        """
```

## Base Interfaces

Book Reader uses interfaces (abstract base classes) to define the contract for services:

```python
class BaseTTSService(ABC):
    """Base interface for TTS services."""

    @abstractmethod
    def convert_text_to_speech(
        self,
        text: str,
        audio_config: AudioConfig,
        output_path: Optional[str] = None
    ) -> bytes:
        """Convert text to speech."""
        pass
```

For complete implementation details of these services, please refer to the source code.
