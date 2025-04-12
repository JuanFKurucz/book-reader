# Integration Tests for Book Reader

This directory contains integration tests that run the full end-to-end flow of the Book Reader application, including real API calls to OpenAI's TTS service.

## Important Notes

- These tests consume OpenAI API credits when run.
- They are skipped by default during normal test runs.
- They require an OpenAI API key.

## Running Integration Tests

To run the integration tests:

```bash
# Set your OpenAI API key (required)
export OPENAI_API_KEY=your-api-key

# Create sample files and run tests
python -m integration_tests.run_integration_tests --create-samples
```

### Command Line Options

- `--create-samples`: Create sample files before running tests
- `--skip-no-key`: Skip tests if OPENAI_API_KEY is not set (instead of failing)

## Sample Files

The tests require sample files for each document type. These files are:

- PDF: `books/sample.pdf` (should already exist)
- Text: `books/sample.txt` (created by the sample creation script)
- EPUB: `books/sample.epub` (must be provided manually)

## GitHub Actions

Integration tests are configured to run automatically on:

1. Release creation (tags starting with 'v')
2. Manual workflow dispatch

This ensures that the tests are run before a release is made public, validating that the core functionality works with real API calls.

## Adding New Tests

To add a new integration test:

1. Create a new test function in `test_end_to_end.py`
2. Mark it with `@pytest.mark.expensive`
3. Ensure it handles cleanup of any temporary files
4. Document any special requirements
