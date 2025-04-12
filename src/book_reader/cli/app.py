"""Command-line interface for Book Reader."""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt

from book_reader.config.settings import settings
from book_reader.models.audio_config import AudioConfig, TTSModel, TTSVoice
from book_reader.models.pdf_document import PDFDocument
from book_reader.repositories.pdf_repository import PDFRepository
from book_reader.services.conversion_service import ConversionService

console = Console()


def setup_services() -> tuple[PDFRepository, ConversionService]:
    """Set up the repository and service dependencies.

    Returns:
        A tuple containing the repository and service.
    """
    repository = PDFRepository(str(settings.paths.books_dir))
    service = ConversionService(
        repository, progress_file=str(settings.paths.progress_file)
    )
    return repository, service


def display_pdf_choices(pdf_documents: list[PDFDocument]) -> Optional[PDFDocument]:
    """Display available PDF files and let the user choose one.

    Args:
        pdf_documents: List of available PDF documents

    Returns:
        The selected PDF document or None if user cancels
    """
    if not pdf_documents:
        console.print("[bold red]No PDF files found.[/bold red]")
        return None

    console.print("\n[bold blue]Available PDF files:[/bold blue]")
    console.print(
        Panel(
            "\n".join(
                f"{index}. [bold]{doc.metadata.title}[/bold] by "
                f"{doc.metadata.author} ({doc.metadata.page_count} pages, "
                f"{doc.metadata.date})"
                for index, doc in enumerate(pdf_documents, start=1)
            ),
            title=f"Found {len(pdf_documents)} PDF files",
            border_style="blue",
        )
    )

    while True:
        try:
            choice = Prompt.ask(
                "\nEnter the number of the PDF to convert (or q to quit)", default="1"
            )

            if choice.lower() == "q":
                return None

            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(pdf_documents):
                return pdf_documents[choice_idx]
            else:
                console.print("[bold red]Invalid choice. Please try again.[/bold red]")
        except ValueError:
            console.print("[bold red]Please enter a valid number.[/bold red]")


def _handle_pdf_selection(
    repository: PDFRepository, sample: bool
) -> Optional[PDFDocument]:
    """Handles the logic of selecting a PDF based on user input or sample flag.

    Args:
        repository: The PDF repository instance.
        sample: Boolean indicating if the sample PDF should be used.

    Returns:
        The selected PDFDocument or None if no selection is made or found.
    """
    if sample:
        sample_doc = repository.find_by_filename("sample.pdf")
        if not sample_doc:
            console.print(
                "[bold red]Sample file 'sample.pdf' not found in "
                "books directory.[/bold red]"
            )
            return None
        console.print("[bold green]Using sample.pdf for testing.[/bold green]")
        return sample_doc
    else:
        pdf_documents = repository.find_all_pdfs()
        if not pdf_documents:
            console.print(
                f"[bold red]No PDF files found in "
                f"{settings.paths.books_dir}.[/bold red]"
            )
            console.print("Please add PDF files to this directory and try again.")
            return None
        return display_pdf_choices(pdf_documents)


def process_document(
    pdf_document: PDFDocument,
    conversion_service: ConversionService,
    output_dir: Path,
    max_pages: Optional[int] = None,
    batch_size: Optional[int] = None,
    voice: Optional[str] = None,
    model: Optional[str] = None,
    resume: bool = False,
) -> None:
    """Process a PDF document and convert it to an audiobook.

    Args:
        pdf_document: The PDF document to process
        conversion_service: The conversion service
        output_dir: Output directory for audio files
        max_pages: Maximum number of pages to process
        batch_size: Number of chunks to process in parallel
        voice: Voice to use for TTS
        model: Model to use for TTS
        resume: Whether to resume from previous conversion
    """
    # Use batch size from settings if not provided
    effective_batch_size = batch_size if batch_size is not None else settings.batch_size

    meta = pdf_document.metadata
    audio_model_str = model or settings.audio.model
    audio_voice_str = voice or settings.audio.voice

    # Validate and convert model/voice strings to enums
    try:
        audio_model_enum = TTSModel(audio_model_str)
    except ValueError:
        console.print(
            f"[bold yellow]Warning: Invalid TTS model '{audio_model_str}'. "
            f"Using default.[/bold yellow]"
        )
        audio_model_enum = TTSModel(settings.audio.model)

    try:
        audio_voice_enum = TTSVoice(audio_voice_str)
    except ValueError:
        console.print(
            f"[bold yellow]Warning: Invalid TTS voice '{audio_voice_str}'. "
            f"Using default.[/bold yellow]"
        )
        audio_voice_enum = TTSVoice(settings.audio.voice)

    console.print(
        Panel(
            f"[bold green]Converting[/bold green]: {meta.title}\n"
            f"[bold]Author[/bold]: {meta.author}\n"
            f"[bold]Pages[/bold]: {meta.page_count}"
            + (f" (processing first {max_pages})" if max_pages else "")
            + "\n"
            f"[bold]Model[/bold]: {audio_model_enum}\n"
            f"[bold]Voice[/bold]: {audio_voice_enum}\n"
            f"[bold]Batch size[/bold]: {effective_batch_size}\n"
            f"[bold]Resume[/bold]: {'Yes' if resume else 'No'}",
            title="Book Reader Conversion",
            border_style="blue",
        )
    )

    # Create audio configuration using enums
    audio_config = AudioConfig(
        model=audio_model_enum,
        voice=audio_voice_enum,
        max_text_length=settings.audio.max_text_length,
    )

    # Convert PDF to audiobook with progress tracking
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}[/bold blue]"),
        console=console,
    ) as progress:
        task = progress.add_task("Converting PDF to audiobook...", total=None)

        audio_files = conversion_service.convert_pdf_to_audiobook(
            pdf_document=pdf_document,
            output_dir=output_dir,
            audio_config=audio_config,
            batch_size=effective_batch_size,
            resume=resume,
            max_pages=max_pages,
        )

        progress.update(task, completed=True)

    # Print summary
    console.print("\n[bold green]Conversion completed![/bold green]")

    # Calculate file count safely
    file_count = 0
    if audio_files is not None:
        if isinstance(audio_files, list):
            file_count = len(audio_files)

    console.print(
        f"[green]Generated {file_count} audio files in "
        f"{output_dir}/{pdf_document.book_id}[/green]"
    )


@click.group()
@click.version_option("0.1.0", prog_name="book-reader")
def cli() -> None:
    """Book Reader - Convert PDF files to audio using OpenAI TTS."""
    pass


@cli.command()
@click.option(
    "--sample", is_flag=True, help="Use sample.pdf from the books directory for testing"
)
@click.option(
    "--max-pages", type=int, default=None, help="Maximum number of pages to process"
)
@click.option(
    "--batch-size",
    type=int,
    default=None,
    help=f"Batch size for parallel processing (default: {settings.batch_size})",
)
@click.option(
    "--voice",
    type=str,
    default=None,
    help=f"Voice to use (default: {settings.audio.voice})",
)
@click.option(
    "--model",
    type=str,
    default=None,
    help=f"Model to use (default: {settings.audio.model})",
)
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False),
    default=None,
    help=f"Directory to save audiobooks (default: {settings.paths.output_dir})",
)
@click.option(
    "--books-dir",
    type=click.Path(file_okay=False),
    default=None,
    help=f"Directory containing PDF files (default: {settings.paths.books_dir})",
)
@click.option("--resume", is_flag=True, help="Resume previous conversion")
def convert(
    sample: bool,
    max_pages: Optional[int],
    batch_size: Optional[int],
    voice: Optional[str],
    model: Optional[str],
    output_dir: Optional[str],
    books_dir: Optional[str],
    resume: bool,
) -> None:
    """Convert PDF files to audiobooks."""
    # Update settings if command line options are provided
    if books_dir:
        settings.paths.books_dir = Path(books_dir)
    if output_dir:
        settings.paths.output_dir = Path(output_dir)
    if voice:
        settings.audio.voice = voice
    if model:
        settings.audio.model = model
    if batch_size:
        settings.batch_size = batch_size

    # Ensure directories exist
    settings.paths.books_dir.mkdir(parents=True, exist_ok=True)
    settings.paths.output_dir.mkdir(parents=True, exist_ok=True)

    # Set up services
    repository, service = setup_services()

    # Handle PDF selection
    selected_pdf = _handle_pdf_selection(repository, sample)

    if not selected_pdf:
        console.print(
            "[bold yellow]No PDF selected for conversion. Exiting.[/bold yellow]"
        )
        sys.exit(1)

    # Process the selected document
    if max_pages:
        console.print(f"[bold blue]Processing first {max_pages} pages.[/bold blue]")

    process_document(
        pdf_document=selected_pdf,
        conversion_service=service,
        output_dir=settings.paths.output_dir,
        max_pages=max_pages,
        batch_size=batch_size,
        voice=voice,
        model=model,
        resume=resume,
    )


@cli.command()
def list_pdfs() -> None:
    """List all available PDF files."""
    repository, _ = setup_services()
    pdf_documents = repository.find_all_pdfs()

    if not pdf_documents:
        console.print(
            f"[bold red]No PDF files found in {settings.paths.books_dir}.[/bold red]"
        )
        console.print("Please add PDF files to this directory and try again.")
        return

    console.print("\n[bold blue]Available PDF files:[/bold blue]")
    console.print(
        Panel(
            "\n".join(
                f"{index}. [bold]{doc.metadata.title}[/bold] by "
                f"{doc.metadata.author} ({doc.metadata.page_count} pages, "
                f"{doc.metadata.date})"
                for index, doc in enumerate(pdf_documents, start=1)
            ),
            title=f"Found {len(pdf_documents)} PDF files",
            border_style="blue",
        )
    )


def main() -> None:
    """Run the Book Reader CLI application."""
    try:
        cli()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
