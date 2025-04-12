"""PDF to Audiobook Conversion Service."""

import concurrent.futures
import json
import os
from pathlib import Path
from typing import List, Optional, Sequence, Union

from book_reader.models.audio_config import AudioConfig
from book_reader.models.pdf_document import PDFDocument
from book_reader.repositories.pdf_repository import PDFRepository
from book_reader.services.tts_service import OpenAITTSServiceFactory, TTSService
from book_reader.utils.logging import get_logger
from book_reader.utils.text_processing import TextProcessor

logger = get_logger(__name__)

# Use Sequence for covariance if only iteration is needed
ChunkData = tuple[str, Path, int, AudioConfig]
ChunkArgs = Sequence[ChunkData]  # Sequence of chunk data tuples


class ConversionService:
    """Service for converting PDFs to audiobooks."""

    def __init__(
        self,
        pdf_repository: PDFRepository,
        tts_service: Optional[TTSService] = None,
        progress_file: str = "conversion_progress.json",
        batch_size: int = 4,
    ) -> None:
        """Initialize the conversion service.

        Args:
            pdf_repository: Repository for accessing PDFs
            tts_service: Service for text-to-speech conversion
            progress_file: File to store conversion progress
            batch_size: Number of parallel conversions
        """
        self.pdf_repository = pdf_repository
        # Use provided TTS service or create one
        self.tts_service = tts_service or OpenAITTSServiceFactory.create()
        self.progress_file = Path(progress_file)
        self.text_processor = TextProcessor()
        self.batch_size = batch_size
        self.current_book_id: Optional[str] = None

    def convert_pdf_to_audiobook(
        self,
        pdf_document: PDFDocument,
        output_dir: Path,
        audio_config: Optional[AudioConfig] = None,
        batch_size: int = 4,
        resume: bool = False,
        max_pages: Optional[int] = None,
    ) -> Optional[Path]:
        """Convert PDF to audiobook.

        Args:
            pdf_document: PDF document to convert
            output_dir: Directory to save audiobook files
            audio_config: Audio configuration
            batch_size: Number of parallel conversions
            resume: Whether to resume previous conversion
            max_pages: Maximum number of pages to process

        Returns:
            Path to the output directory
        """
        # Load PDF content ONCE
        loaded_pdf_document = self.pdf_repository.load_pages(
            pdf_document=pdf_document, max_pages=max_pages
        )
        if not loaded_pdf_document.pages:
            logger.warning(f"No pages loaded for {pdf_document.file_name}. Exiting.")
            return None

        # Set current book ID
        self.current_book_id = loaded_pdf_document.book_id

        # Create output directory
        book_output_dir = output_dir / loaded_pdf_document.book_id
        book_output_dir.mkdir(parents=True, exist_ok=True)

        # Ensure audio_config is not None before passing
        if audio_config is None:
            logger.warning("No AudioConfig provided, using defaults.")
            _audio_config = AudioConfig()
        else:
            _audio_config = audio_config

        # Prepare chunks (pass loaded doc)
        all_text_chunks = self._prepare_text_chunks(loaded_pdf_document, _audio_config)

        # Assign chunks to pages (Optional: if needed later, but split from all_text)
        # This part might need revisiting if page-specific chunk association
        # is critical
        # For now, we work with the flat list `all_text_chunks`

        # Prepare conversion data using the flat list of chunks
        all_chunks_data = self._prepare_chunks_for_conversion(
            all_text_chunks, book_output_dir, _audio_config
        )

        # Load previous progress if resuming
        completed_chunks_indices: list[int] = (
            self._load_progress(loaded_pdf_document.book_id) if resume else []
        )

        # Filter out already completed chunks
        chunks_to_process: List[ChunkData] = [
            chunk_data
            for chunk_data in all_chunks_data
            if chunk_data[2] not in completed_chunks_indices
        ]

        if not chunks_to_process:
            logger.info("All chunks already processed or no chunks to process.")
            return None

        # Determine processing method
        if batch_size > 1:
            logger.info(
                f"Processing {len(chunks_to_process)} chunks in parallel "
                f"(batch size: {batch_size})"
            )
            audio_files = self._process_chunks_in_parallel(
                chunks_to_process, batch_size
            )
        else:
            logger.info(f"Processing {len(chunks_to_process)} chunks serially.")
            audio_files = self._process_chunks_sequentially(
                chunks_to_process, batch_size
            )

        # Update progress
        # Get indices of successfully processed chunks for saving progress
        successful_indices: set[int] = {
            idx for _, _, idx, _ in chunks_to_process[: len(audio_files)]
        }
        # Combine completed and newly successful
        all_completed_indices = list(set(completed_chunks_indices) | successful_indices)

        # Save progress with the combined set
        self._save_progress(loaded_pdf_document.book_id, all_completed_indices)

        logger.info(
            f"Audiobook conversion for '{loaded_pdf_document.book_id}' completed."
        )
        # Return the output directory instead of the list of files
        # for compatibility with tests
        return book_output_dir

    def _prepare_text_chunks(
        self, loaded_pdf_document: PDFDocument, audio_config: AudioConfig
    ) -> List[str]:
        """Extract text from loaded pages and return individual chunks.

        Each page's chunks are preserved separately to maintain proper
        chunking structure.
        """
        # Instead of concatenating all pages, preserve each page's chunks
        all_chunks = []
        for page in loaded_pdf_document.pages:
            if hasattr(page, "chunks") and page.chunks:
                all_chunks.extend(page.chunks)
            else:
                # Use content if chunks not available
                max_length = audio_config.max_text_length
                page_chunks = self.text_processor.split_into_chunks(
                    page.content, max_length=max_length
                )
                all_chunks.extend(page_chunks)

        return all_chunks

    def _prepare_chunks_for_conversion(
        self, text_chunks: List[str], output_dir: Path, audio_config: AudioConfig
    ) -> List[ChunkData]:
        """Prepare chunk data tuples for processing."""
        return [
            (chunk, output_dir, index, audio_config)
            for index, chunk in enumerate(text_chunks)
        ]

    def _process_chunks(
        self,
        chunks_to_process: Sequence[ChunkData],
        batch_size: int,
    ) -> list[Path]:
        """Process text chunks serially."""
        audio_files: list[Path] = []
        completed_indices: list[int] = []
        for args in chunks_to_process:
            try:
                audio_file = self._process_chunk_worker(args)
                if audio_file:
                    audio_files.append(audio_file)
                    completed_indices.append(args[2])
            except Exception as e:
                logger.error(f"Error processing chunk {args[2] + 1}: {e}")
        # Progress saving logic moved or handled after parallel/serial call
        return audio_files

    def _process_chunk_worker(
        self, args: ChunkData
    ) -> Optional[Path]:  # Return Optional[Path]
        chunk, output_path, chunk_index, config = args
        # config should not be None if prepared correctly
        # if config is None: # Add safety check if necessary
        #     logger.error(f"Missing config for chunk {chunk_index + 1}")
        #     return None
        try:
            output_file = self.tts_service.synthesize(
                text=chunk,
                output_path=output_path,
                chunk_index=chunk_index,
                config=config,
            )
            return output_file  # synthesize should return Path or raise
        except Exception as e:
            logger.error(f"Error processing chunk {chunk_index + 1}: {e}")
            return None  # Return None on error

    def _process_chunks_in_parallel(
        self,
        chunks_to_process: Sequence[ChunkData],
        batch_size: int,
    ) -> list[Path]:
        """Process text chunks in parallel using ThreadPoolExecutor."""
        num_chunks = len(list(chunks_to_process))
        audio_files_results: list[Union[Path, None]] = [None] * num_chunks
        processed_count = 0
        chunks_list = list(chunks_to_process)
        processed_indices: list[int] = []  # Track successful indices

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=min(batch_size, os.cpu_count() or 1)
        ) as executor:
            future_to_index = {
                executor.submit(self._process_chunk_worker, args): index
                for index, args in enumerate(chunks_list)
            }

            for future in concurrent.futures.as_completed(future_to_index):
                original_index = future_to_index[future]
                chunk_display_index = chunks_list[original_index][2] + 1
                try:
                    result = future.result()
                    if result:  # Check if worker returned a Path
                        audio_files_results[original_index] = result
                        logger.info(
                            f"Successfully processed chunk {chunk_display_index}."
                        )
                        processed_count += 1
                        # Add index on success
                        processed_indices.append(chunks_list[original_index][2])
                    else:
                        # Worker returned None (error occurred within worker)
                        logger.error(
                            f"Chunk {chunk_display_index} failed processing "
                            f"(worker error)."
                        )
                except Exception as e:
                    # Error during future.result() itself
                    logger.error(
                        f"Error processing chunk {chunk_display_index} in parallel: {e}"
                    )

        # Save progress using the list of successfully processed indices

        successful_files: list[Path] = [p for p in audio_files_results if p is not None]
        logger.info(
            f"Parallel processing finished. "
            f"Successful: {len(successful_files)}, "
            f"Errors: {num_chunks - len(successful_files)}"
        )
        return successful_files

    def _process_chunks_sequentially(
        self,
        chunks_to_process: Sequence[ChunkData],
        batch_size: int,
    ) -> list[Path]:
        """Process text chunks serially."""
        return self._process_chunks(chunks_to_process, batch_size)

    def _load_progress(self, book_id: str) -> list[int]:  # Return list[int]
        """Load conversion progress from file.

        Args:
            book_id: Book ID

        Returns:
            List of completed chunk indices
        """
        if not self.progress_file.exists():
            return []

        try:
            with open(self.progress_file, "r") as f:
                progress_data = json.load(f)
                # Expecting a structure like {"book_id": [0, 1, 2]}
                book_progress_list = progress_data.get(book_id, [])
                if isinstance(book_progress_list, list) and all(
                    isinstance(i, int) for i in book_progress_list
                ):
                    return book_progress_list  # Return list directly
                else:
                    logger.warning(f"Invalid progress data for {book_id}, resetting.")
                    return []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_progress(self, book_id: str, completed_indices: list[int]) -> None:
        """Save conversion progress to file.

        Args:
            book_id: Book ID
            completed_indices: List of completed chunk indices
        """
        progress = {}
        if self.progress_file.exists():
            try:
                with open(self.progress_file, "r") as f:
                    # Read the entire file content
                    content = f.read()
                    # Check if the content is empty before trying to load JSON
                    if content:
                        progress = json.loads(content)
                    else:
                        progress = {}
            except (json.JSONDecodeError, FileNotFoundError):
                logger.warning(
                    f"Could not load or parse existing progress from "
                    f"{self.progress_file}"
                )
                progress = {}
            except Exception as e:  # Catch other potential file reading errors
                logger.error(f"Error reading progress file {self.progress_file}: {e}")
                progress = {}

        # Update progress - store as sorted list for JSON compatibility
        progress[book_id] = sorted(completed_indices)

        # Save progress
        try:
            with open(self.progress_file, "w") as f:
                json.dump(progress, f)
        except IOError as e:
            logger.error(f"Could not save progress to {self.progress_file}: {e}")

    def prepare_chunks_for_conversion(
        self, pdf_document: PDFDocument, completed_chunks: list[int]
    ) -> List[ChunkData]:
        """Prepare chunks for conversion, filtering completed chunks.

        Public wrapper around the internal methods used to prepare chunks.

        Args:
            pdf_document: PDF document to process
            completed_chunks: List of indices of completed chunks

        Returns:
            List of chunk data tuples, excluding completed chunks
        """
        # Load the document if needed (tests might have already loaded it)
        loaded_pdf_document = pdf_document
        if not pdf_document.pages and hasattr(pdf_document, "file_path"):
            loaded_pdf_document = self.pdf_repository.load_pages(pdf_document)

        # Create dummy output directory for tests
        output_dir = Path("test_output") / loaded_pdf_document.book_id

        # Use a default audio config
        audio_config = AudioConfig()

        # Prepare text chunks from loaded document
        all_text_chunks = self._prepare_text_chunks(loaded_pdf_document, audio_config)

        # Convert to chunk data format
        all_chunks_data = self._prepare_chunks_for_conversion(
            all_text_chunks, output_dir, audio_config
        )

        # Filter out completed chunks
        chunks_to_process = [
            chunk_data
            for chunk_data in all_chunks_data
            if chunk_data[2] not in completed_chunks
        ]

        return chunks_to_process
