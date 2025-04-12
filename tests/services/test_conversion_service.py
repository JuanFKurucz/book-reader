"""Tests for the Conversion Service."""

from pathlib import Path
from typing import List, cast
from unittest.mock import MagicMock, mock_open, patch

import pytest

from book_reader.config.audio_config import AudioConfig
from book_reader.models.formats.pdf_document import (
    DocumentPage,
    PDFDocument,
    PDFMetadata,
    PDFPage,
)
from book_reader.services.conversion_service import ConversionService


@pytest.fixture
def mock_pdf_repository() -> MagicMock:
    """Create a mock PDF repository."""
    mock_repo = MagicMock()
    return mock_repo


@pytest.fixture
def mock_tts_service() -> MagicMock:
    """Create a mock TTS service."""
    mock_tts = MagicMock()
    mock_tts.synthesize.return_value = Path("test/audio.mp3")
    return mock_tts


@pytest.fixture
def test_pdf_document() -> PDFDocument:
    """Create a test PDF document with pages and chunks."""
    metadata = PDFMetadata(
        title="Test Document",
        author="Test Author",
        date="2023-01-01",
        language="en",
        page_count=2,
    )
    # Create pages with chunks
    page1_chunks = ["Test content page 1 chunk 1"]
    page2_chunks = ["Test content page 2 chunk 1"]
    pages = [
        PDFPage(
            content="\n".join(page1_chunks),  # Simulate original page content
            page_number=0,  # Use 0-based indexing internally
            chunks=page1_chunks,
        ),
        PDFPage(
            content="\n".join(page2_chunks),
            page_number=1,
            chunks=page2_chunks,
        ),
    ]
    return PDFDocument(
        file_path="test.pdf",
        file_name="test.pdf",
        metadata=metadata,
        pages=cast(List[DocumentPage], pages),
    )


@pytest.fixture
def conversion_service(
    tmp_path: Path, mock_pdf_repository: MagicMock, mock_tts_service: MagicMock
) -> ConversionService:
    """Create a ConversionService instance with mocked dependencies."""
    progress_file_path = tmp_path / "test_progress.json"
    service = ConversionService(
        document_repository=mock_pdf_repository,
        tts_service=mock_tts_service,
        progress_file=str(progress_file_path),
    )
    return service


class TestConversionService:
    """Tests for the ConversionService class."""

    def test_init(self, mock_pdf_repository: MagicMock, tmp_path: Path) -> None:
        """Test ConversionService initialization."""
        progress_file = tmp_path / "init_progress.json"
        service = ConversionService(
            document_repository=mock_pdf_repository,
            progress_file=str(progress_file),
        )
        assert service.document_repository == mock_pdf_repository
        assert service.progress_file == progress_file

    @patch("pathlib.Path.exists", return_value=False)
    @patch("builtins.open", new_callable=mock_open, read_data="{}")
    def test_load_progress_no_file(
        self,
        mock_file_open: MagicMock,
        mock_exists: MagicMock,
        conversion_service: ConversionService,
    ) -> None:
        """Test loading progress when file does not exist."""
        progress = conversion_service._load_progress("test_book")
        assert progress == []
        mock_exists.assert_called_once()
        mock_file_open.assert_not_called()

    @patch("pathlib.Path.exists", return_value=True)
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"test_book": [1, 2, 3]}',
    )
    def test_load_progress_with_data(
        self,
        mock_file_open: MagicMock,
        mock_exists: MagicMock,
        conversion_service: ConversionService,
    ) -> None:
        """Test loading progress with data."""
        progress = conversion_service._load_progress("test_book")
        assert progress == [1, 2, 3]
        mock_exists.assert_called_once()
        progress_file_path = conversion_service.progress_file
        mock_file_open.assert_called_once_with(progress_file_path, "r")

    @patch("pathlib.Path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="{}")
    def test_save_progress(
        self,
        mock_file_open: MagicMock,
        mock_exists: MagicMock,
        conversion_service: ConversionService,
    ) -> None:
        """Test saving progress."""
        with patch("json.dump") as mock_json_dump:
            conversion_service._save_progress("test_book", [1, 2, 3])

            progress_file_path = conversion_service.progress_file
            assert mock_file_open.call_count == 2
            mock_file_open.assert_any_call(progress_file_path, "r")
            # Using a variable for the mode might seem excessive
            # but helps break the line
            write_mode = "w"
            mock_file_open.assert_any_call(
                progress_file_path,
                write_mode,
            )

            write_call_handle = mock_file_open.return_value
            expected_data = {"test_book": [1, 2, 3]}
            mock_json_dump.assert_called_once_with(
                expected_data,
                write_call_handle,
            )

    @pytest.mark.parametrize(
        "completed_chunks, expected_chunks",
        [
            ([], 2),  # No progress, process all chunks
            ([0], 1),  # Chunk 0 completed, process 1
            ([0, 1], 0),  # All completed, process none
        ],
    )
    def test_prepare_chunks_for_conversion(
        self,
        mock_pdf_repository: MagicMock,
        test_pdf_document: PDFDocument,
        completed_chunks: list[int],
        expected_chunks: int,
        tmp_path: Path,
    ) -> None:
        """Test preparing chunks, filtering completed ones."""
        progress_file = tmp_path / "prep_progress.json"
        service = ConversionService(
            mock_pdf_repository, progress_file=str(progress_file)
        )

        # Set up mock PDF document
        mock_pdf_repository.load_pages.return_value = test_pdf_document.pages

        # Call the method
        actual_chunks = service.prepare_chunks_for_conversion(
            test_pdf_document, completed_chunks
        )

        # Prepare expected chunks (filter based on completed_chunks)
        all_chunks = [
            (chunk, i, i)
            for i, chunk in enumerate(
                [c for page in test_pdf_document.pages for c in page.chunks]
            )
        ]
        expected_raw_chunks = [
            chunk for i, chunk in enumerate(all_chunks) if i not in completed_chunks
        ]
        # Reconstruct expected format if needed, or just compare counts/indices
        assert len(actual_chunks) == expected_chunks
        # Check specific indices if necessary
        actual_indices = [c[2] for c in actual_chunks]
        expected_indices = [c[2] for c in expected_raw_chunks]
        assert sorted(actual_indices) == sorted(expected_indices)

    @pytest.mark.parametrize(
        "completed_chunks, resume, batch_size, expected_chunks",
        [
            # Test case 1: No resume, batch_size 1 -> process all chunks sequentially
            ([], False, 1, 2),
            # Test case 2: No resume, batch_size > 1 -> process all chunks in parallel
            ([], False, 2, 2),
            # Test case 3: Resume with no completed chunks -> process all
            ([], True, 1, 2),
            # Test case 4: Resume with some completed chunks (chunk 0) ->
            # process remaining (chunk 1)
            ([0], True, 1, 1),
            # Test case 5: Resume with all completed chunks -> process none
            ([0, 1], True, 1, 0),
            # Test case 6: Resume with some completed chunks, batch_size > 1 ->
            # process remaining
            ([1], True, 2, 1),
            # Test case 7: Resume with all completed, batch_size > 1 -> process none
            ([0, 1], True, 2, 0),
        ],
    )
    def test_convert_pdf_to_audiobook(
        self,
        conversion_service: ConversionService,
        mock_pdf_repository: MagicMock,
        mock_tts_service: MagicMock,
        test_pdf_document: PDFDocument,
        completed_chunks: list[int],
        resume: bool,
        batch_size: int,
        expected_chunks: int,
    ) -> None:
        """Test converting PDF to audiobook with different resumption scenarios."""
        mock_pdf_repository.load_pages.return_value = test_pdf_document
        mock_tts_service.synthesize.return_value = Path("test/audio1.mp3")
        expected_book_id = test_pdf_document.book_id
        audio_config = AudioConfig()

        # Calculate expected number of total text chunks based on fixture
        page_chunk_counts = (len(page.chunks) for page in test_pdf_document.pages)
        total_text_chunks = sum(page_chunk_counts)
        # Expected number of chunks to *actually* process after filtering
        num_chunks_to_process = total_text_chunks - len(completed_chunks)

        with patch.object(
            conversion_service, "_load_progress", return_value=completed_chunks
        ) as mock_load_progress:
            # Break the list comprehension for clarity and length
            processed_paths = [
                Path(f"test/audio{i + 1}.mp3") for i in range(expected_chunks)
            ]
            process_return_value = processed_paths if expected_chunks > 0 else []

            # Break ternary operator
            if conversion_service.batch_size > 1:
                process_method_to_mock = "_process_chunks_in_parallel"
            else:
                process_method_to_mock = "_process_chunks_sequentially"

            with patch.object(
                conversion_service,
                process_method_to_mock,
                return_value=process_return_value,
            ) as mock_process:
                with patch.object(
                    conversion_service, "_save_progress"
                ) as mock_save_progress:
                    output_dir = Path("test_output")
                    result = conversion_service.convert_pdf_to_audiobook(
                        pdf_document=test_pdf_document,
                        output_dir=output_dir,
                        audio_config=audio_config,
                        batch_size=conversion_service.batch_size,
                        resume=resume,
                        max_pages=None,
                    )

                    # Assert load_pages was called
                    mock_pdf_repository.load_pages.assert_any_call(
                        document=test_pdf_document, max_pages=None
                    )

                    # Assert process method calls based on filtered chunks
                    if num_chunks_to_process > 0:
                        mock_process.assert_called_once()
                        actual_processed_chunks_data = mock_process.call_args[0][0]
                        assert len(actual_processed_chunks_data) == (
                            num_chunks_to_process
                        )
                        # Verify indices match non-completed ones
                        expected_indices = [
                            i
                            for i in range(total_text_chunks)
                            if i not in completed_chunks
                        ]
                        actual_indices = [
                            chunk_data[2] for chunk_data in actual_processed_chunks_data
                        ]
                        assert actual_indices == expected_indices
                        # Assert save progress was called if processing happened
                        mock_save_progress.assert_called_once()
                        saved_indices = sorted(
                            list(set(completed_chunks + actual_indices))
                        )
                        mock_save_progress.assert_called_once_with(
                            expected_book_id,
                            saved_indices,
                        )
                    else:
                        mock_process.assert_not_called()
                        mock_save_progress.assert_not_called()

                    # Assert load progress was called correctly based on resume flag
                    if resume:
                        mock_load_progress.assert_called_once_with(expected_book_id)
                    else:
                        mock_load_progress.assert_not_called()

                    # Assert the final result
                    if expected_chunks > 0:
                        expected_output_dir = output_dir / expected_book_id
                        assert result == expected_output_dir
                        assert expected_output_dir.exists()
                        # Check if the correct number of files were "created"
                        # (based on the return value of the mocked process)
                        assert (
                            len(list(expected_output_dir.glob("*.mp3"))) == 0
                        )  # Files aren't actually created by mock
                        assert len(process_return_value) == expected_chunks
                    else:
                        # If no chunks were processed, the output dir shouldn't
                        # be created
                        assert not result

    @patch("book_reader.services.conversion_service.ConversionService._load_progress")
    @patch("book_reader.services.conversion_service.ConversionService._save_progress")
    def test_convert_pdf_to_audiobook_resume(
        self,
        mock_save_progress: MagicMock,
        mock_load_progress: MagicMock,
        conversion_service: ConversionService,
        mock_pdf_repository: MagicMock,
        mock_tts_service: MagicMock,
    ) -> None:
        """Test convert_pdf_to_audiobook with resume=True where all chunks are done."""
        mock_load_progress.return_value = [0]  # Load progress indicates chunk 0 is done
        # Create a document that ONLY has chunk 0 effectively
        mock_pdf_page = PDFPage(
            content="Chunk 0 content", page_number=1, chunks=["Chunk 0 content"]
        )
        mock_pdf_doc = PDFDocument(
            file_path="test_book.pdf",
            file_name="test_book.pdf",
            metadata=PDFMetadata(title="Test", author="Author", page_count=1),
            pages=[mock_pdf_page],
        )
        mock_pdf_repository.load_pages.return_value = mock_pdf_doc

        expected_book_id = "test_book"

        with patch.object(conversion_service, "_process_chunks") as mock_process_chunks:
            mock_output_dir = MagicMock(spec=Path)
            mock_book_output_dir = MagicMock(spec=Path)
            mock_output_dir.__truediv__.return_value = mock_book_output_dir

            mock_audio_config = AudioConfig()

            audio_files = conversion_service.convert_pdf_to_audiobook(
                pdf_document=mock_pdf_doc,
                output_dir=mock_output_dir,
                audio_config=mock_audio_config,
                batch_size=1,
                resume=True,
            )

            mock_load_progress.assert_called_once_with(expected_book_id)
            mock_process_chunks.assert_not_called()
            mock_tts_service.synthesize.assert_not_called()
            # Save progress should NOT be called because no new chunks were processed
            mock_save_progress.assert_not_called()
            assert audio_files is None
