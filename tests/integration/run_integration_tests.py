#!/usr/bin/env python
"""Run integration tests for Book Reader.

This script runs the integration tests, which are marked as expensive
and skipped by default in normal pytest runs.

The tests interact with OpenAI's API and consume credits.
"""

import argparse
import os
import subprocess
import sys

from dotenv import load_dotenv


def main() -> int:
    """Run integration tests."""
    parser = argparse.ArgumentParser(
        description="Run integration tests for Book Reader"
    )
    parser.add_argument(
        "--create-samples",
        action="store_true",
        help="Create sample files before running tests",
    )
    parser.add_argument(
        "--skip-no-key",
        action="store_true",
        help="Skip tests if OPENAI_API_KEY is not set instead of failing",
    )
    args = parser.parse_args()

    # Try to load API key from .env file
    load_dotenv()

    # Check for API key
    if "OPENAI_API_KEY" not in os.environ:
        if args.skip_no_key:
            print("OPENAI_API_KEY not set. Skipping integration tests.")
            return 0
        else:
            print(
                "Error: OPENAI_API_KEY environment variable not set. "
                "Integration tests require an OpenAI API key."
            )
            return 1

    # Create sample files if requested
    if args.create_samples:
        print("Creating sample files...")
        subprocess.run([sys.executable, "-m", "tests.integration.create_samples"])

    # Run the integration tests
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/integration",
        "-v",
        "-m",
        "expensive",
    ]
    result = subprocess.run(cmd)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
