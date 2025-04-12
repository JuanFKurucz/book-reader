"""Command-line interface for Book Reader."""

import sys
from pathlib import Path
from typing import Any, List, Optional, Tuple, cast

import click
from rich.console import Console
from rich.prompt import Prompt

from book_reader.config import settings
from book_reader.config.audio_config import AudioConfig
from book_reader.models.base.document import BaseDocument
from book_reader.repositories.document_factory import DocumentFactory
from book_reader.services.conversion_service import ConversionService
from book_reader.services.tts_service import OpenAITTSServiceFactory

console = Console()


def setup_services() -> Tuple[DocumentFactory, ConversionService]:
    """Set up and return the document factory and conversion service."""
    # Create the document factory
    document_factory = DocumentFactory()

    # Create the TTS service
    tts_service = OpenAITTSServiceFactory.create()

    # Create the conversion service with the repositories
    conversion_service = ConversionService(
        tts_service=tts_service,
        # Cast to make type checker happy - document_factory is not BaseRepository
        # but this still works at runtime due to design
        document_repository=cast(Any, document_factory),
    )

    return document_factory, conversion_service


def _handle_sample_document(
    factory: DocumentFactory, books_dir_path: Path
) -> Optional[BaseDocument]:
    """Handle selection of sample document.

    Args:
        factory: The document factory to use
        books_dir_path: Directory containing document files

    Returns:
        Sample document or None if not found
    """
    # Use the sample document
    sample_files = list(books_dir_path.glob("sample.*"))
    if not sample_files:
        err_msg = f"No sample document found in {books_dir_path}"
        console.print(f"[bold red]Error:[/bold red] {err_msg}")
        return None

    # Convert Path to string for factory
    repo = factory.get_repository_for_file(
        str(sample_files[0]),
        books_dir=str(books_dir_path),
    )

    if repo is None:
        console.print(
            "[bold red]Error:[/bold red] Could not get repository for sample file"
        )
        return None

    sample_doc = repo.find_by_filename(sample_files[0].name)
    if sample_doc:
        console.print(
            f"[bold green]Using sample document:[/bold green] {sample_doc.file_name}"
        )
        return cast(BaseDocument, sample_doc)
    else:
        msg = "[bold red]Error:[/bold red] Could not load sample document"
        console.print(msg)
        return None


def _handle_specific_document(
    factory: DocumentFactory, books_dir_path: Path, filename: str
) -> Optional[BaseDocument]:
    """Handle selection of a specific document by filename.

    Args:
        factory: The document factory to use
        books_dir_path: Directory containing document files
        filename: Specific filename to convert

    Returns:
        Selected document or None if selection failed
    """
    # User specified a filename
    doc_path = books_dir_path / filename
    if not doc_path.exists():
        msg = f"[bold red]Error:[/bold red] File not found: {doc_path}"
        console.print(msg)
        return None

    # Convert Path to string for factory
    repository = factory.get_repository_for_file(
        str(doc_path),
        books_dir=str(books_dir_path),
    )
    if not repository:
        err_msg = f"Unsupported file format: {doc_path}"
        console.print(f"[bold red]Error:[/bold red] {err_msg}")
        return None

    document = repository.find_by_filename(doc_path.name)
    if document:
        console.print(
            f"[bold green]Selected document:[/bold green] {document.file_name}"
        )
        return cast(BaseDocument, document)
    else:
        err_msg = f"Could not load document: {doc_path}"
        console.print(f"[bold red]Error:[/bold red] {err_msg}")
        return None


def _handle_interactive_selection(
    factory: DocumentFactory, books_dir_path: Path
) -> Optional[BaseDocument]:
    """Handle interactive document selection.

    Args:
        factory: The document factory to use
        books_dir_path: Directory containing document files

    Returns:
        Selected document or None if selection failed
    """
    # No specific document selected, show a list
    all_documents: List[BaseDocument] = []
    for repository in factory.get_all_repositories(books_dir=str(books_dir_path)):
        all_documents.extend(repository.find_all_documents())

    if not all_documents:
        console.print(
            f"[bold yellow]No documents found in {books_dir_path}[/bold yellow]"
        )
        return None

    # Display documents with numbers
    console.print("[bold]Available documents:[/bold]")
    for i, doc in enumerate(all_documents, 1):
        console.print(f"  {i}. {doc.file_name} ({doc.format})")

    # Prompt user to select a document
    try:
        prompt = "Enter document number to convert"
        selection = Prompt.ask(prompt, default="1")
        index = int(selection) - 1
        if 0 <= index < len(all_documents):
            selected_doc = all_documents[index]
            console.print(
                f"[bold green]Selected document:[/bold green] {selected_doc.file_name}"
            )
            return selected_doc
        else:
            console.print("[bold red]Error:[/bold red] Invalid selection")
            return None
    except (ValueError, KeyboardInterrupt):
        msg = "[bold yellow]Document selection canceled[/bold yellow]"
        console.print(msg)
        return None


def _handle_document_selection(
    factory: DocumentFactory,
    use_sample: bool = False,
    filename: Optional[str] = None,
    books_dir: Optional[Path] = None,
) -> Optional[BaseDocument]:
    """Handle document selection logic.

    Args:
        factory: The document factory to use
        use_sample: Whether to use the sample document
        filename: Specific filename to convert
        books_dir: Directory containing document files

    Returns:
        Selected document or None if selection failed
    """
    # Get books directory from settings if not specified
    if books_dir is None:
        books_dir_path = Path("books")  # Default to books/ in current directory
        # Try to get books_dir from settings if available
        if hasattr(settings, "paths"):
            if hasattr(settings.paths, "books_dir"):
                books_dir_path = settings.paths.books_dir
    else:
        books_dir_path = books_dir

    if use_sample:
        return _handle_sample_document(factory, books_dir_path)
    elif filename:
        return _handle_specific_document(factory, books_dir_path, filename)
    else:
        return _handle_interactive_selection(factory, books_dir_path)


def _create_audio_config(
    voice: Optional[str] = None, model: Optional[str] = None
) -> AudioConfig:
    """Create audio configuration based on provided values or settings.

    Args:
        voice: Voice to use for TTS
        model: TTS model to use

    Returns:
        Audio configuration
    """
    default_voice = "alloy"
    default_model = "tts-1"

    if hasattr(settings, "audio"):
        if hasattr(settings.audio, "voice"):
            default_voice = settings.audio.voice
        if hasattr(settings.audio, "model"):
            default_model = settings.audio.model

    voice_str = voice if voice else default_voice
    model_str = model if model else default_model

    # Use the from_strings method to properly convert string values to enums
    return AudioConfig.from_strings(
        model_str=model_str,
        voice_str=voice_str,
    )


def process_document(
    document: BaseDocument,
    conversion_service: ConversionService,
    output_dir: Path,
    max_pages: Optional[int] = None,
    batch_size: Optional[int] = None,
    voice: Optional[str] = None,
    model: Optional[str] = None,
    resume: bool = False,
) -> None:
    """Process a document with the conversion service.

    Args:
        document: Document to process
        conversion_service: Service to use for conversion
        output_dir: Directory to save output files
        max_pages: Maximum number of pages to process
        batch_size: Batch size for parallel processing
        voice: Voice to use for TTS
        model: TTS model to use
        resume: Whether to resume previous conversion
    """
    # Create directories if they don't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create directories in settings if they exist
    if hasattr(settings, "paths"):
        if hasattr(settings.paths, "books_dir"):
            settings.paths.books_dir.mkdir(parents=True, exist_ok=True)
        if hasattr(settings.paths, "output_dir"):
            settings.paths.output_dir.mkdir(parents=True, exist_ok=True)

    # Configure audio settings
    audio_config = _create_audio_config(voice=voice, model=model)

    if max_pages:
        msg = f"[bold blue]Processing first {max_pages} pages.[/bold blue]"
        console.print(msg)

    # Set batch size, use provided value or get from settings if available
    effective_batch_size = batch_size
    if effective_batch_size is None and hasattr(settings, "batch_size"):
        effective_batch_size = settings.batch_size
    if effective_batch_size is None:
        effective_batch_size = 4  # Default

    # Convert document to audiobook
    conversion_service.convert_document_to_audiobook(
        document=document,
        output_dir=output_dir,
        audio_config=audio_config,
        batch_size=effective_batch_size,
        resume=resume,
        max_pages=max_pages,
    )


@click.group()
def cli() -> None:
    """Book Reader - Convert documents to audiobooks using OpenAI TTS."""
    pass


@cli.command()
@click.argument("filename", required=False)
@click.option(
    "--sample",
    is_flag=True,
    help="Use the sample document for testing",
)
@click.option(
    "--max-pages",
    type=int,
    help="Maximum number of pages to process",
)
@click.option(
    "--batch-size",
    type=int,
    help="Batch size for parallel processing",
)
@click.option(
    "--voice",
    type=str,
    help="Voice to use for TTS",
)
@click.option(
    "--model",
    type=str,
    help="TTS model to use",
)
@click.option(
    "--output-dir",
    type=click.Path(),
    help="Directory to save audiobook files",
)
@click.option(
    "--books-dir",
    type=click.Path(exists=True),
    help="Directory containing document files",
)
@click.option(
    "--resume",
    is_flag=True,
    help="Resume previous conversion",
)
def convert(
    filename: Optional[str] = None,
    sample: bool = False,
    max_pages: Optional[int] = None,
    batch_size: Optional[int] = None,
    voice: Optional[str] = None,
    model: Optional[str] = None,
    output_dir: Optional[str] = None,
    books_dir: Optional[str] = None,
    resume: bool = False,
) -> None:
    """Convert a document to an audiobook.

    If FILENAME is provided, converts that specific document.
    If --sample is provided, uses the sample document.
    Otherwise, presents a list of available documents to choose from.
    """
    # Set up paths from settings or command line arguments
    books_dir_path = Path("books")  # Default to books/ in current directory
    output_dir_path = Path("output")  # Default to output/ in current directory

    # If settings.paths exists, use its values as defaults
    if hasattr(settings, "paths"):
        if hasattr(settings.paths, "books_dir"):
            books_dir_path = settings.paths.books_dir
        if hasattr(settings.paths, "output_dir"):
            output_dir_path = settings.paths.output_dir

    # Override with command line arguments if provided
    if books_dir:
        books_dir_path = Path(books_dir)
    if output_dir:
        output_dir_path = Path(output_dir)

    # Set up services
    document_factory, conversion_service = setup_services()

    # Handle document selection
    document = _handle_document_selection(
        factory=document_factory,
        use_sample=sample,
        filename=filename,
        books_dir=books_dir_path,
    )

    if not document:
        sys.exit(1)

    # Process the selected document
    process_document(
        document=document,
        conversion_service=conversion_service,
        output_dir=output_dir_path,
        max_pages=max_pages,
        batch_size=batch_size,
        voice=voice,
        model=model,
        resume=resume,
    )

    msg = "\n[bold green]Conversion completed successfully![/bold green]"
    console.print(msg)


def main() -> None:
    """Main entry point."""
    try:
        cli()
    except KeyboardInterrupt:
        msg = "\n[bold yellow]Operation cancelled by user.[/bold yellow]"
        console.print(msg)
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
