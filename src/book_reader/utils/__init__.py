"""Utility functions for the Book Reader application."""

from book_reader.utils.console import console
from book_reader.utils.logging import get_logger
from book_reader.utils.text_processing import TextProcessor

__all__ = ["get_logger", "TextProcessor", "console"]
