# Models

This page documents the data models used in the Book Reader application.

## AudioConfig

```python
class AudioConfig:
    """Configuration for audio conversion.

    Attributes:
        voice: The voice to use for TTS ("alloy", "echo", "fable", "nova", "onyx", "shimmer")
        model: The TTS model to use ("tts-1", "tts-1-hd")
        speed: The speed factor for audio playback (0.5 to 2.0)
        format: The audio format ("mp3", "wav")
    """
```

## PDFDocument

```python
class PDFDocument:
    """Represents a PDF document.

    Attributes:
        path: Path to the PDF file
        filename: Filename of the PDF
        metadata: Dictionary containing document metadata
    """
```

## PDFPage

```python
class PDFPage:
    """Represents a page from a PDF document.

    Attributes:
        page_number: The page number (1-indexed)
        content: The extracted text content of the page
        document: Reference to the parent PDFDocument
    """
```

## ConversionStatus

```python
class ConversionStatus:
    """Tracks the status of a PDF to audiobook conversion.

    Attributes:
        total_pages: Total number of pages in the document
        processed_pages: Number of pages that have been processed
        current_batch: Current batch being processed
        start_time: When the conversion started
        completed_chunks: List of completed chunk files
    """
```

## ConversionResult

```python
class ConversionResult:
    """Results of a PDF to audiobook conversion.

    Attributes:
        document: The PDF document that was converted
        output_files: List of generated audio files
        duration_seconds: Total duration of the audiobook in seconds
        total_pages: Total number of pages processed
        audio_config: The audio configuration used
    """
```

## TextChunk

```python
class TextChunk:
    """A chunk of text to be processed by the TTS service.

    Attributes:
        content: The text content
        chunk_id: Unique identifier for the chunk
        page_numbers: List of page numbers contained in this chunk
        output_path: Path where the resulting audio will be saved
    """
```

For complete implementation details of these models, please refer to the source code.
