"""Create sample files for integration tests."""

from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from tests.integration.conftest import EPUB_SAMPLE, PDF_SAMPLE, TEXT_SAMPLE


def create_sample_pdf_file() -> None:
    """Create a sample PDF file for testing."""
    books_dir = Path("books")
    sample_pdf = books_dir / PDF_SAMPLE

    # Create books directory if it doesn't exist
    books_dir.mkdir(exist_ok=True)

    # Only create the file if it doesn't already exist
    if not sample_pdf.exists():
        # Create a simple PDF with reportlab
        c = canvas.Canvas(str(sample_pdf), pagesize=letter)
        c.setFont("Helvetica", 16)
        c.drawString(100, 750, "Sample PDF Document")

        c.setFont("Helvetica", 12)
        msg = "This is a sample PDF document for testing purposes."
        c.drawString(100, 700, msg)

        # Add a couple paragraphs of text
        y_position = 650
        for i in range(1, 3):
            c.setFont("Helvetica-Bold", 14)
            c.drawString(100, y_position, f"Chapter {i}")
            y_position -= 30

            c.setFont("Helvetica", 12)
            paragraph = (
                f"This is paragraph {i} of the sample document. "
                "It contains multiple sentences to be converted to audio. "
                "The text is simple to ensure fast conversion. "
                "The sentences vary in length and content to test the "
                "TTS service."
            )

            # Simple text wrapping
            words = paragraph.split()
            line = ""
            for word in words:
                test_line = line + word + " "
                if len(test_line) > 60:  # Crude line length limit
                    c.drawString(100, y_position, line)
                    y_position -= 20
                    line = word + " "
                else:
                    line = test_line

            if line:
                c.drawString(100, y_position, line)

            y_position -= 40

        c.save()
        print(f"Created sample PDF file: {sample_pdf}")
    else:
        print(f"Sample PDF file already exists: {sample_pdf}")


def create_sample_text_file() -> None:
    """Create a sample text file for testing."""
    books_dir = Path("books")
    sample_txt = books_dir / TEXT_SAMPLE

    # Create books directory if it doesn't exist
    books_dir.mkdir(exist_ok=True)

    # Only create the file if it doesn't already exist
    if not sample_txt.exists():
        with open(sample_txt, "w") as f:
            f.write("# Sample Text Document\n\n")
            f.write("This is a sample text document for testing purposes.\n\n")
            f.write("## Chapter 1\n\n")
            f.write("This is the first chapter of the sample document.\n")
            msg = "It contains multiple sentences to be converted to audio.\n"
            f.write(msg)
            f.write(
                "The sentences vary in length and content to test the TTS service.\n\n"
            )
            f.write("## Chapter 2\n\n")
            f.write("This is the second chapter of the sample document.\n")
            f.write("It also contains multiple sentences for testing.\n")
            f.write("The text is simple to ensure fast conversion.\n")

        print(f"Created sample text file: {sample_txt}")
    else:
        print(f"Sample text file already exists: {sample_txt}")


def create_sample_epub_file() -> None:
    """
    For EPUB, this is more complex as it's a binary format.
    We'd need an external library like ebooklib to create one.

    For testing purposes, we can provide instructions on where to get a sample.
    """
    print(
        "EPUB sample creation requires external dependencies. "
        "Please manually provide a sample EPUB file named "
        f"'{EPUB_SAMPLE}' in the books directory."
    )


if __name__ == "__main__":
    # Create sample files
    create_sample_pdf_file()
    create_sample_text_file()
    create_sample_epub_file()
