#!/usr/bin/env python
"""Simple runner script for PDF to Audiobook converter."""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from book_reader.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
