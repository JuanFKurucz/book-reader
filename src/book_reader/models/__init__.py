"""Models package."""

# Base models
from book_reader.models.base.document import (
    BaseDocument,
    DocumentMetadata,
    DocumentPage,
)
from book_reader.models.formats.epub_document import EPUBDocument

# Format-specific models
from book_reader.models.formats.pdf_document import PDFDocument, PDFMetadata, PDFPage
from book_reader.models.formats.text_document import TextDocument

# Note: Audio config is now in config package
# from book_reader.config.audio_config import (
#     AudioConfig,
#     TTSModel,
#     TTSVoice,
# )

__all__ = [
    # Base models
    "BaseDocument",
    "DocumentMetadata",
    "DocumentPage",
    # Format-specific models
    "PDFDocument",
    "PDFMetadata",
    "PDFPage",
    "EPUBDocument",
    "TextDocument",
    # Audio config models are exported via config package now
    # "AudioConfig", "TTSModel", "TTSVoice",
]
