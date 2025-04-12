#!/usr/bin/env python
"""Run integration tests for Book Reader.

This script runs the integration tests, which are marked as expensive
and skipped by default in normal pytest runs.

The tests will interact with OpenAI's API and consume credits, so use with caution.
"""

import argparse
import os
import subprocess
import sys


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
        subprocess.run([sys.executable, "-m", "integration_tests.create_samples"])

    # Run the integration tests
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "integration_tests",
        "-v",
        "-m",
        "expensive",
    ]
    result = subprocess.run(cmd)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
