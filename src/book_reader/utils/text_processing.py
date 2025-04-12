"""Text Processing Utilities."""

import re
from typing import List


class TextProcessor:
    """Utility class for text processing operations."""

    @staticmethod
    def split_into_chunks(text: str, max_length: int) -> List[str]:
        """Split text into chunks of maximum length, preserving sentences.

        Args:
            text: Text to split into chunks
            max_length: Maximum length of each chunk

        Returns:
            List of text chunks
        """
        if not text.strip():
            return []

        # Split into sentences (handling various punctuation)
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if not sentence:  # Skip empty sentences from split
                continue

            # If a single sentence exceeds max_length, split it forcefully
            if len(sentence) > max_length:
                # Add any existing current_chunk first
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""

                # Split the long sentence
                start = 0
                while start < len(sentence):
                    end = min(start + max_length, len(sentence))
                    # Try to find a space to break at near the end
                    break_point = sentence.rfind(" ", start, end)
                    if break_point == -1 or end == len(sentence):
                        final_end = end
                    else:
                        final_end = break_point

                    chunks.append(sentence[start:final_end].strip())
                    start = final_end + 1  # Move past the space
                continue  # Move to the next sentence

            # If adding the sentence fits, append it
            if (
                not current_chunk
                or len(current_chunk) + len(sentence) + 1 <= max_length
            ):
                current_chunk += sentence + " "  # Add space between sentences
            # If adding the sentence exceeds length, finalize current chunk
            # and start new
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + " "

        # Add the last remaining chunk
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean text by removing extra whitespace and empty lines.

        Args:
            text: Text to clean

        Returns:
            Cleaned text
        """
        lines = text.split("\n")
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        cleaned_text = "\n".join(cleaned_lines)
        return cleaned_text

    @staticmethod
    def truncate_text(text: str, max_length: int) -> str:
        """Truncate text to maximum length, trying to keep complete sentences.

        Args:
            text: Text to truncate
            max_length: Maximum length

        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text

        # Try to truncate at a sentence boundary
        truncated = text[:max_length]
        last_period = truncated.rfind(".")

        if last_period > 0:
            return truncated[: last_period + 1]

        # If no sentence boundary found, truncate at the max length
        return truncated
