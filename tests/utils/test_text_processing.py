"""Tests for the TextProcessor utility."""

import pytest
from book_reader.utils.text_processing import TextProcessor


@pytest.fixture
def text_processor() -> TextProcessor:
    """Create a TextProcessor instance."""
    return TextProcessor()


class TestTextProcessor:
    """Tests for the TextProcessor class."""

    def test_split_into_chunks_empty(self, text_processor: TextProcessor) -> None:
        """Test splitting empty text."""
        assert text_processor.split_into_chunks("", 100) == []
        assert text_processor.split_into_chunks("   ", 100) == []

    def test_split_into_chunks_short(self, text_processor: TextProcessor) -> None:
        """Test splitting text shorter than max length."""
        text = "This is a short text."
        assert text_processor.split_into_chunks(text, 100) == [text]

    def test_split_into_chunks_exact(self, text_processor: TextProcessor) -> None:
        """Test splitting text exactly matching max length."""
        text = "This fits exactly."
        assert text_processor.split_into_chunks(text, len(text)) == [text]

    def test_split_into_chunks_long_sentence(
        self, text_processor: TextProcessor
    ) -> None:
        """Test splitting a single sentence longer than max length."""
        text = "This is a very long sentence that must be split forcefully."
        max_len = 20
        result = text_processor.split_into_chunks(text, max_len)
        assert len(result) > 1
        for chunk in result:
            assert len(chunk) <= max_len
        # Check if the text is roughly reconstructed
        assert "".join(result).replace(" ", "") == text.replace(" ", "")

    def test_split_into_chunks_multiple(self, text_processor: TextProcessor) -> None:
        """Test splitting text into multiple chunks."""
        text = "This is a sentence. " * 10  # Multiple sentences
        max_len = 60
        result = text_processor.split_into_chunks(text, max_len)

        assert len(result) > 1
        for chunk in result:
            assert len(chunk) <= max_len

        # Compare reconstructed text after normalizing whitespace
        reconstructed = " ".join(result)
        original_normalized = " ".join(text.split())
        assert reconstructed == original_normalized

    def test_split_into_chunks_punctuation(self, text_processor: TextProcessor) -> None:
        """Test splitting text with various punctuation."""
        text = "Sentence one. Sentence two! Sentence three? Sentence four."
        result = text_processor.split_into_chunks(text, 20)
        assert len(result) == 4
        assert result[0] == "Sentence one."
        assert result[1] == "Sentence two!"
        assert result[2] == "Sentence three?"
        assert result[3] == "Sentence four."

    def test_clean_text_simple(self, text_processor: TextProcessor) -> None:
        """Test simple text cleaning."""
        text = "  Hello   World  \n\n How are you? \n"
        expected = "Hello   World\nHow are you?"
        assert text_processor.clean_text(text) == expected

    def test_clean_text_empty(self, text_processor: TextProcessor) -> None:
        """Test cleaning empty text."""
        assert text_processor.clean_text("") == ""
        assert text_processor.clean_text(" \n ") == ""

    def test_truncate_text_short(self, text_processor: TextProcessor) -> None:
        """Test truncating text shorter than max length."""
        text = "Short text."
        assert text_processor.truncate_text(text, 100) == text

    def test_truncate_text_exact(self, text_processor: TextProcessor) -> None:
        """Test truncating text at exact length."""
        text = "Exact length."
        assert text_processor.truncate_text(text, len(text)) == text

    def test_truncate_text_long_sentence_boundary(
        self, text_processor: TextProcessor
    ) -> None:
        """Test truncating longer text at a sentence boundary."""
        text = "This is the first sentence. This is the second."
        expected = "This is the first sentence."
        assert text_processor.truncate_text(text, 30) == expected

    def test_truncate_text_long_no_boundary(
        self, text_processor: TextProcessor
    ) -> None:
        """Test truncating longer text without a nearby sentence boundary."""
        text = "This is a very long sentence without clear breaks"
        # The function returns the exact slice if no period is found.
        # For max_length=20, this slice includes the trailing space.
        expected = "This is a very long "
        assert text_processor.truncate_text(text, 20) == expected

    def test_clean_text_single_line(self, text_processor: TextProcessor) -> None:
        """Test cleaning a single line of text."""
        result = text_processor.clean_text("  Hello, world!  ")
        assert result == "Hello, world!"

    def test_clean_text_multi_line(self, text_processor: TextProcessor) -> None:
        """Test cleaning multiple lines of text."""
        text = """
        Line 1

        Line 2
          Line 3
        """
        result = text_processor.clean_text(text)
        assert result == "Line 1\nLine 2\nLine 3"

    def test_split_into_chunks_exact_length(
        self, text_processor: TextProcessor
    ) -> None:
        """Test splitting text exactly at max length."""
        text = "A" * 100
        result = text_processor.split_into_chunks(text, 100)
        assert result == [text]
