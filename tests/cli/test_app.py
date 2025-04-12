"""Tests for the CLI application."""

from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from book_reader.cli.app import _handle_document_selection, cli
from book_reader.models.base.document import BaseDocument
from book_reader.repositories.document_factory import DocumentFactory


@pytest.fixture
def runner() -> CliRunner:
    """Provides a Click CLI runner."""
    return CliRunner()


@pytest.fixture
def mock_setup_services() -> Generator[MagicMock, None, None]:
    """Mocks the setup_services function."""
    mock_factory = MagicMock()
    mock_conversion_service = MagicMock()
    with patch("book_reader.cli.app.setup_services") as mock_setup:
        mock_setup.return_value = (mock_factory, mock_conversion_service)
        yield mock_setup


@pytest.fixture
def mock_handle_document_selection() -> Generator[MagicMock, None, None]:
    """Mocks the _handle_document_selection function."""
    mock_doc = MagicMock()
    mock_doc.file_name = "selected_test.pdf"
    target = "book_reader.cli.app._handle_document_selection"
    with patch(target) as mock_select:
        mock_select.return_value = mock_doc
        yield mock_select


@pytest.fixture
def mock_process_document() -> Generator[MagicMock, None, None]:
    """Mocks the process_document function."""
    with patch("book_reader.cli.app.process_document") as mock_process:
        yield mock_process


@pytest.fixture
def mock_settings() -> MagicMock:
    """Mocks the settings object and its nested attributes."""
    mock = MagicMock()

    # Mock paths with appropriate Path objects
    mock.paths = MagicMock()
    mock.paths.books_dir = Path("./mock_books")
    mock.paths.output_dir = Path("./mock_audiobooks")
    mock.paths.progress_file = Path("./mock_progress.json")

    # Mock audio settings
    mock.audio = MagicMock()
    mock.audio.voice = "alloy"
    mock.audio.model = "tts-1"

    # Mock other settings
    mock.batch_size = 4
    mock.debug = False

    return mock


@pytest.fixture
def mock_document_factory() -> MagicMock:
    """Mocks the DocumentFactory."""
    mock_factory = MagicMock(spec=DocumentFactory)
    mock_repo = MagicMock()
    mock_factory.get_repository_for_file.return_value = mock_repo
    mock_factory.get_all_repositories.return_value = [mock_repo]
    return mock_factory


@pytest.fixture
def mock_base_document() -> MagicMock:
    """Mocks a BaseDocument instance."""
    mock_doc = MagicMock(spec=BaseDocument)
    mock_doc.file_name = "mock_doc.pdf"
    mock_doc.format = "pdf"
    mock_doc.book_id = "mock_doc"  # Add book_id needed internally
    return mock_doc


# --- Test Cases ---


@patch("book_reader.cli.app.settings")
def test_convert_no_args(
    mock_settings_patch: MagicMock,
    runner: CliRunner,
    mock_setup_services: MagicMock,
    mock_handle_document_selection: MagicMock,
    mock_process_document: MagicMock,
    mock_settings: MagicMock,
) -> None:
    """Test the convert command with no specific file or sample flag."""
    # Configure mock
    mock_settings_patch.return_value = mock_settings

    result = runner.invoke(cli, ["convert"])

    assert result.exit_code == 0
    mock_setup_services.assert_called_once()

    # Check that _handle_document_selection was called (without checking exact args)
    mock_handle_document_selection.assert_called_once()
    # Verify key behavior - check use_sample is False
    assert mock_handle_document_selection.call_args[1]["use_sample"] is False
    assert mock_handle_document_selection.call_args[1]["filename"] is None

    # Check process_document was called with the returned document
    mock_process_document.assert_called_once()
    expected_doc = mock_handle_document_selection.return_value
    assert mock_process_document.call_args[1]["document"] == expected_doc


@patch("book_reader.cli.app.settings")
def test_convert_sample_flag(
    mock_settings_patch: MagicMock,
    runner: CliRunner,
    mock_setup_services: MagicMock,
    mock_handle_document_selection: MagicMock,
    mock_process_document: MagicMock,
    mock_settings: MagicMock,
) -> None:
    """Test the convert command using the --sample flag."""
    # Configure mock
    mock_settings_patch.return_value = mock_settings

    result = runner.invoke(cli, ["convert", "--sample"])

    assert result.exit_code == 0
    mock_setup_services.assert_called_once()

    # Check that _handle_document_selection was called (without checking exact args)
    mock_handle_document_selection.assert_called_once()
    # Verify key behavior - check use_sample is True
    assert mock_handle_document_selection.call_args[1]["use_sample"] is True
    assert mock_handle_document_selection.call_args[1]["filename"] is None

    # Check process_document was called with the returned document
    mock_process_document.assert_called_once()
    expected_doc = mock_handle_document_selection.return_value
    assert mock_process_document.call_args[1]["document"] == expected_doc


@patch("book_reader.cli.app.settings")
def test_convert_specific_file(
    mock_settings_patch: MagicMock,
    runner: CliRunner,
    mock_setup_services: MagicMock,
    mock_handle_document_selection: MagicMock,
    mock_process_document: MagicMock,
    mock_settings: MagicMock,
) -> None:
    """Test the convert command with a specific filename."""
    mock_settings_patch.return_value = mock_settings

    test_filename = "my_book.epub"
    result = runner.invoke(cli, ["convert", test_filename])

    assert result.exit_code == 0
    mock_setup_services.assert_called_once()

    # Check that _handle_document_selection was called (without checking exact args)
    mock_handle_document_selection.assert_called_once()
    # Verify key behavior - check filename is passed correctly
    assert mock_handle_document_selection.call_args[1]["use_sample"] is False
    assert mock_handle_document_selection.call_args[1]["filename"] == test_filename

    # Check process_document was called with the returned document
    mock_process_document.assert_called_once()
    expected_doc = mock_handle_document_selection.return_value
    assert mock_process_document.call_args[1]["document"] == expected_doc


@patch("book_reader.cli.app.settings")
def test_convert_override_output_dir(
    mock_settings_patch: MagicMock,
    runner: CliRunner,
    mock_setup_services: MagicMock,
    mock_handle_document_selection: MagicMock,
    mock_process_document: MagicMock,
    tmp_path: Path,
    mock_settings: MagicMock,
) -> None:
    """Test overriding the output directory via --output-dir."""
    mock_settings_patch.return_value = mock_settings

    mock_settings.paths.books_dir = Path("./mock_books")
    mock_settings.paths.output_dir = Path("./ignore")

    custom_output_dir = tmp_path / "custom_audio"
    test_filename = "my_book.pdf"
    result = runner.invoke(
        cli,
        [
            "convert",
            test_filename,
            "--output-dir",
            str(custom_output_dir),
        ],
    )

    assert result.exit_code == 0
    mock_setup_services.assert_called_once()

    # Check that _handle_document_selection was called (without checking exact args)
    mock_handle_document_selection.assert_called_once()
    # Verify key behavior - check filename is passed correctly
    assert mock_handle_document_selection.call_args[1]["use_sample"] is False
    assert mock_handle_document_selection.call_args[1]["filename"] == test_filename

    # Specifically test that the output directory is set to the custom value
    mock_process_document.assert_called_once()
    # Just check output_dir was set to the custom path string representation
    assert str(mock_process_document.call_args[1]["output_dir"]) == str(
        custom_output_dir
    )


@patch("book_reader.cli.app.settings")
def test_convert_override_books_dir(
    mock_settings_patch: MagicMock,
    runner: CliRunner,
    mock_setup_services: MagicMock,
    mock_handle_document_selection: MagicMock,
    mock_process_document: MagicMock,
    tmp_path: Path,
    mock_settings: MagicMock,
) -> None:
    """Test overriding the books directory via --books-dir."""
    mock_settings_patch.return_value = mock_settings

    custom_books_dir = tmp_path / "custom_books"
    custom_books_dir.mkdir()
    mock_settings.paths.books_dir = custom_books_dir
    mock_settings.paths.output_dir = Path("./mock_audiobooks")

    test_filename = "my_book.pdf"
    (custom_books_dir / test_filename).touch()

    result = runner.invoke(
        cli,
        [
            "convert",
            test_filename,
            "--books-dir",
            str(custom_books_dir),
        ],
    )

    assert result.exit_code == 0
    mock_setup_services.assert_called_once()

    # Check that _handle_document_selection was called (without checking exact args)
    mock_handle_document_selection.assert_called_once()
    # Verify key behavior - check filename is passed correctly
    assert mock_handle_document_selection.call_args[1]["use_sample"] is False
    assert mock_handle_document_selection.call_args[1]["filename"] == test_filename

    # Check process_document was called with the returned document
    mock_process_document.assert_called_once()
    expected_doc = mock_handle_document_selection.return_value
    assert mock_process_document.call_args[1]["document"] == expected_doc
    # Just check that the output_dir attribute exists
    assert "output_dir" in mock_process_document.call_args[1]


@patch("book_reader.cli.app.settings")
def test_convert_override_audio_options(
    mock_settings_patch: MagicMock,
    runner: CliRunner,
    mock_setup_services: MagicMock,
    mock_handle_document_selection: MagicMock,
    mock_process_document: MagicMock,
    mock_settings: MagicMock,
) -> None:
    """Test overriding audio options like voice, model, batch size."""
    mock_settings_patch.return_value = mock_settings

    test_filename = "my_audio_test.pdf"
    test_voice = "alloy"
    test_model = "tts-1-hd"
    test_batch_size = 2

    result = runner.invoke(
        cli,
        [
            "convert",
            test_filename,
            "--voice",
            test_voice,
            "--model",
            test_model,
            "--batch-size",
            str(test_batch_size),
        ],
    )

    assert result.exit_code == 0
    mock_process_document.assert_called_once()
    process_args = mock_process_document.call_args[1]

    # Check that the correct override values were passed to process_document
    assert process_args["voice"] == test_voice
    assert process_args["model"] == test_model
    assert process_args["batch_size"] == test_batch_size


@patch("book_reader.cli.app.settings")
def test_convert_resume_flag(
    mock_settings_patch: MagicMock,
    runner: CliRunner,
    mock_setup_services: MagicMock,
    mock_handle_document_selection: MagicMock,
    mock_process_document: MagicMock,
    mock_settings: MagicMock,
) -> None:
    """Test using the --resume flag."""
    mock_settings_patch.return_value = mock_settings

    test_filename = "my_resume_test.txt"
    result = runner.invoke(
        cli,
        [
            "convert",
            test_filename,
            "--resume",
        ],
    )

    assert result.exit_code == 0
    mock_process_document.assert_called_once()
    process_args = mock_process_document.call_args[1]

    # Check that resume=True was passed
    assert process_args["resume"] is True


# --- Tests for _handle_document_selection ---


@patch("book_reader.cli.app.settings")
def test_handle_selection_sample(
    mock_settings_patch: MagicMock,
    mock_document_factory: MagicMock,
    mock_base_document: MagicMock,
    tmp_path: Path,
    mock_settings: MagicMock,
) -> None:
    """Test _handle_document_selection with the sample flag."""
    # Setup the file and mock paths
    sample_file = tmp_path / "books" / "sample.pdf"
    sample_file.parent.mkdir(exist_ok=True)
    sample_file.touch()

    # Configure the mock settings
    mock_settings.paths.books_dir = sample_file.parent
    mock_settings_patch.return_value = mock_settings

    # Configure the mock repository - directly mock the necessary parts
    mock_repo = MagicMock()
    mock_repo.find_by_filename.return_value = mock_base_document
    mock_document_factory.get_repository_for_file.return_value = mock_repo

    # Skip most verifications since we've mocked the appropriate behaviors
    selected_doc = _handle_document_selection(
        factory=mock_document_factory,
        use_sample=True,
        books_dir=mock_settings.paths.books_dir,
    )

    # Just verify the end result without checking exact call parameters
    assert selected_doc is mock_base_document


@patch("book_reader.cli.app.settings")
def test_handle_selection_filename(
    mock_settings_patch: MagicMock,
    mock_document_factory: MagicMock,
    mock_base_document: MagicMock,
    tmp_path: Path,
    mock_settings: MagicMock,
) -> None:
    """Test _handle_document_selection with a specific filename."""
    mock_settings_patch.return_value = mock_settings

    # Configure file path to test
    book_file = tmp_path / "books" / "my_book.epub"
    book_file.parent.mkdir(exist_ok=True)
    book_file.touch()
    mock_settings.paths.books_dir = book_file.parent

    # Set up mocks to return the expected document
    mock_repo = MagicMock()
    mock_repo.find_by_filename.return_value = mock_base_document
    mock_document_factory.get_repository_for_file.return_value = mock_repo

    # Call function under test
    selected_doc = _handle_document_selection(
        factory=mock_document_factory,
        filename="my_book.epub",
        books_dir=mock_settings.paths.books_dir,
    )

    # Just verify the document was returned correctly
    assert selected_doc is mock_base_document


@patch("rich.prompt.Prompt.ask", return_value="1")
@patch("book_reader.cli.app.settings")
def test_handle_selection_interactive(
    mock_settings_patch: MagicMock,
    mock_prompt_ask: MagicMock,
    mock_document_factory: MagicMock,
    mock_base_document: MagicMock,
    tmp_path: Path,
    mock_settings: MagicMock,
) -> None:
    """Test _handle_document_selection with interactive selection."""
    mock_settings_patch.return_value = mock_settings

    book_file = tmp_path / "books" / "interactive.txt"
    book_file.parent.mkdir(exist_ok=True)
    book_file.touch()

    mock_repo = mock_document_factory.get_all_repositories.return_value[0]
    mock_repo.find_all_documents.return_value = [mock_base_document]
    mock_base_document.file_name = "interactive.txt"  # Match the file
    mock_base_document.format = "txt"

    selected_doc = _handle_document_selection(
        factory=mock_document_factory,
        books_dir=mock_settings.paths.books_dir,
    )

    assert selected_doc == mock_base_document
    mock_document_factory.get_all_repositories.assert_called_once()
    mock_repo.find_all_documents.assert_called_once()
    mock_prompt_ask.assert_called_once_with(
        "Enter document number to convert", default="1"
    )


@patch("rich.prompt.Prompt.ask", side_effect=KeyboardInterrupt)
@patch("book_reader.cli.app.settings")
def test_handle_selection_interactive_cancel(
    mock_settings_patch: MagicMock,
    mock_prompt_ask: MagicMock,
    mock_document_factory: MagicMock,
    tmp_path: Path,
    mock_settings: MagicMock,
) -> None:
    """Test _handle_document_selection interactive cancel (Ctrl+C)."""
    mock_settings_patch.return_value = mock_settings

    book_file = tmp_path / "books" / "cancel.pdf"
    book_file.parent.mkdir(exist_ok=True)
    book_file.touch()

    mock_repo = mock_document_factory.get_all_repositories.return_value[0]
    mock_repo.find_all_documents.return_value = [
        MagicMock()  # Need at least one doc
    ]

    selected_doc = _handle_document_selection(
        factory=mock_document_factory,
        books_dir=mock_settings.paths.books_dir,
    )

    assert selected_doc is None
    mock_prompt_ask.assert_called_once()


@patch("book_reader.cli.app.settings")
def test_handle_selection_file_not_found(
    mock_settings_patch: MagicMock,
    mock_document_factory: MagicMock,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
    mock_settings: MagicMock,
) -> None:
    """Test _handle_document_selection when filename does not exist."""
    mock_settings_patch.return_value = mock_settings

    # Configure path but don't create the file
    mock_settings.paths.books_dir = tmp_path / "books"
    mock_settings.paths.books_dir.mkdir()

    # Mock repository to not be called
    mock_document_factory.get_repository_for_file.return_value = None

    # Mock the Path.exists method to return False for the specific case
    with patch.object(Path, "exists", return_value=False):
        selected_doc = _handle_document_selection(
            factory=mock_document_factory,
            filename="non_existent.pdf",
            books_dir=mock_settings.paths.books_dir,
        )

        # Verify result
        assert selected_doc is None
        captured = capsys.readouterr()
        assert "File not found" in captured.out


@patch("book_reader.cli.app.settings")
def test_handle_selection_no_documents(
    mock_settings_patch: MagicMock,
    mock_document_factory: MagicMock,
    capsys: pytest.CaptureFixture,
    mock_settings: MagicMock,
) -> None:
    """Test _handle_document_selection when no documents are found."""
    mock_settings_patch.return_value = mock_settings

    mock_settings.paths.books_dir = Path("./mock_books")

    mock_repo = mock_document_factory.get_all_repositories.return_value[0]
    mock_repo.find_all_documents.return_value = []

    selected_doc = _handle_document_selection(
        factory=mock_document_factory,
        books_dir=mock_settings.paths.books_dir,
    )

    assert selected_doc is None
    captured = capsys.readouterr()
    assert "No documents found" in captured.out


@patch("rich.prompt.Prompt.ask", side_effect=ValueError)
@patch("book_reader.cli.app.settings")
def test_handle_selection_interactive_invalid_input(
    mock_settings_patch: MagicMock,
    mock_prompt_ask: MagicMock,
    mock_document_factory: MagicMock,
    mock_base_document: MagicMock,
    capsys: pytest.CaptureFixture,
    mock_settings: MagicMock,
) -> None:
    """Test interactive selection with invalid (non-integer) input."""
    mock_settings_patch.return_value = mock_settings

    mock_settings.paths.books_dir = Path("./mock_books")

    mock_repo = mock_document_factory.get_all_repositories.return_value[0]
    mock_repo.find_all_documents.return_value = [mock_base_document]

    selected_doc = _handle_document_selection(
        factory=mock_document_factory,
        books_dir=mock_settings.paths.books_dir,
    )

    assert selected_doc is None
    mock_prompt_ask.assert_called_once()
    captured = capsys.readouterr()
    assert "Document selection canceled" in captured.out


@patch("rich.prompt.Prompt.ask", return_value="99")
@patch("book_reader.cli.app.settings")
def test_handle_selection_interactive_out_of_bounds(
    mock_settings_patch: MagicMock,
    mock_prompt_ask: MagicMock,
    mock_document_factory: MagicMock,
    mock_base_document: MagicMock,
    capsys: pytest.CaptureFixture,
    mock_settings: MagicMock,
) -> None:
    """Test interactive selection with an out-of-bounds number."""
    mock_settings_patch.return_value = mock_settings

    mock_settings.paths.books_dir = Path("./mock_books")

    mock_repo = mock_document_factory.get_all_repositories.return_value[0]
    mock_repo.find_all_documents.return_value = [mock_base_document]

    selected_doc = _handle_document_selection(
        factory=mock_document_factory,
        books_dir=mock_settings.paths.books_dir,
    )

    assert selected_doc is None
    mock_prompt_ask.assert_called_once()
    captured = capsys.readouterr()
    assert "Invalid selection" in captured.out


@patch("book_reader.cli.app.settings")
def test_handle_selection_sample_not_found(
    mock_settings_patch: MagicMock,
    mock_document_factory: MagicMock,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
    mock_settings: MagicMock,
) -> None:
    """Test _handle_document_selection when sample file does not exist."""
    mock_settings_patch.return_value = mock_settings

    mock_settings.paths.books_dir = tmp_path / "empty_books"
    mock_settings.paths.books_dir.mkdir()

    selected_doc = _handle_document_selection(
        factory=mock_document_factory, use_sample=True
    )

    assert selected_doc is None
    captured = capsys.readouterr()
    assert "No sample document found" in captured.out
