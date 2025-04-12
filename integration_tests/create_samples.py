"""Create sample files for integration tests."""

from pathlib import Path

from integration_tests.conftest import EPUB_SAMPLE, TEXT_SAMPLE


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
            f.write("It contains multiple sentences to be converted to audio.\n")
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
    create_sample_text_file()
    create_sample_epub_file()
