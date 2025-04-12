# API Reference

This section provides detailed documentation for Book Reader's Python API. If you want to integrate Book Reader into your own Python applications, these pages will help you understand the available components and how to use them.

## Module Structure

Book Reader is organized into several modules:

- **models**: Data structures used throughout the application
- **repositories**: Components that handle data access and storage
- **services**: Core business logic and processing components
- **utils**: Helper functions and utilities

## Getting Started with the API

To use Book Reader in your own Python scripts:

```python
from book_reader.services.conversion_service import ConversionService
from book_reader.repositories.pdf_repository import PDFRepository
from book_reader.models.audio_config import AudioConfig

# Initialize the repository
pdf_repo = PDFRepository()

# Find a PDF document
pdf_document = pdf_repo.find_by_filename("path/to/your/document.pdf")

# Configure audio settings
audio_config = AudioConfig(
    voice="nova",
    model="tts-1-hd",
    speed=1.0,
    format="mp3"
)

# Initialize the conversion service
conversion_service = ConversionService(
    openai_api_key="your-api-key-here",
    pdf_repository=pdf_repo
)

# Convert the PDF to audiobook
conversion_service.convert_pdf_to_audiobook(
    pdf_document=pdf_document,
    output_dir="path/to/output",
    audio_config=audio_config,
    batch_size=15,
    resume=False,
    max_pages=None
)
```

## Key Components

### ConversionService

The `ConversionService` is the main entry point for the API. It handles the process of converting a PDF document to audio files:

```python
from book_reader.services.conversion_service import ConversionService

conversion_service = ConversionService(
    openai_api_key="your-api-key-here",
    pdf_repository=pdf_repo,
    tts_service=tts_service  # Optional
)
```

### PDFRepository

The `PDFRepository` handles PDF document operations:

```python
from book_reader.repositories.pdf_repository import PDFRepository

pdf_repo = PDFRepository()
pdf_document = pdf_repo.find_by_filename("path/to/your/document.pdf")
pages = pdf_repo.load_pages(pdf_document, page_range=(1, 10))
```

### TTSService

The `TTSService` interfaces with OpenAI's TTS API:

```python
from book_reader.services.tts_service import TTSService
from book_reader.models.audio_config import AudioConfig

audio_config = AudioConfig(voice="nova", model="tts-1")
tts_service = TTSService(api_key="your-api-key-here")
audio_data = tts_service.convert_text_to_speech("Hello world", audio_config)
```

## Error Handling

The API uses a custom exception hierarchy for error handling:

```python
try:
    conversion_service.convert_pdf_to_audiobook(...)
except book_reader.exceptions.PDFReadError as e:
    print(f"Error reading PDF: {e}")
except book_reader.exceptions.TTSError as e:
    print(f"Error in text-to-speech conversion: {e}")
except book_reader.exceptions.BookReaderError as e:
    print(f"General error: {e}")
```

## Advanced Usage

For advanced usage examples and detailed documentation of each component, please refer to the specific module documentation:

- [Models Documentation](models.md)
- [Repositories Documentation](repositories.md)
- [Services Documentation](services.md)
- [Utils Documentation](utils.md)

## Extending Book Reader

Book Reader is designed to be extensible. You can create custom implementations of key interfaces:

```python
from book_reader.repositories.base_repository import BasePDFRepository

class MyCustomPDFRepository(BasePDFRepository):
    def find_by_filename(self, filename: str) -> PDFDocument:
        # Custom implementation
        ...

    def load_pages(self, document: PDFDocument, page_range: Optional[Tuple[int, int]] = None) -> List[PDFPage]:
        # Custom implementation
        ...
```

## Performance Considerations

When working with large documents:

1. Process pages in batches to manage memory usage
2. Enable the resume functionality to handle interruptions
3. Adjust concurrent tasks based on your system's capabilities
4. Consider preprocessing steps for complex PDFs with challenging formatting
