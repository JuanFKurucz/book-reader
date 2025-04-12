# Contributing to Book Reader

First off, thank you for considering contributing to Book Reader! 🎉 It's people like you that make open source projects great.

This document provides guidelines for contributing to this project. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Code of Conduct

This project and everyone participating in it is governed by a [Code of Conduct](CODE_OF_CONDUCT.md) (We'll add this file later!). By participating, you are expected to uphold this code. Please report unacceptable behavior.

## How Can I Contribute?

There are many ways to contribute, from writing code and documentation to reporting bugs and suggesting enhancements.

### Reporting Bugs

- **Ensure the bug was not already reported** by searching on GitHub under [Issues](https://github.com/juanfkurucz/book-reader/issues).
- If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/juanfkurucz/book-reader/issues/new/choose). Be sure to include a **title and clear description**, as much relevant information as possible, and a **code sample or an executable test case** demonstrating the expected behavior that is not occurring. Use the "Bug Report" template.

### Suggesting Enhancements

- Open a new issue using the "Feature Request" template.
- Clearly describe the enhancement and the motivation for it.
- Explain why this enhancement would be useful.
- Include code examples if possible.

### Your First Code Contribution

Unsure where to begin contributing? You can start by looking through these `good first issue` and `help wanted` issues:

- [Good first issues](https://github.com/juanfkurucz/book-reader/labels/good%20first%20issue) - issues which should only require a few lines of code, and a test or two.
- [Help wanted issues](https://github.com/juanfkurucz/book-reader/labels/help%20wanted) - issues which should be a bit more involved than `good first issues`.

### Pull Requests

1.  **Fork the repository** and create your branch from `main`.
2.  **Set up your development environment:**
    - Ensure you have Python 3.13+ installed.
    - It's recommended to use a virtual environment:
      ```bash
      python -m venv .venv
      source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
      ```
    - Install dependencies, including development dependencies:
      ```bash
      # Using uv (recommended)
      uv pip install -e ".[dev]"

      # Or using pip
      pip install -e ".[dev]"
      ```
    - Set up pre-commit hooks (optional but recommended):
      ```bash
      pre-commit install
      ```
3.  **Make your changes.** Ensure your code adheres to the style guides (see below).
4.  **Add tests** for your changes. Ensure the test suite passes.
5.  **Run tests:**
    ```bash
    pytest
    ```
6.  **Ensure code style and quality:**
    - Run the linters and formatters (pre-commit hooks handle this automatically if installed):
      ```bash
      ruff check .
      ruff format .
      mypy src/
      ```
7.  **Update documentation** (README.md, docstrings, etc.) if necessary.
8.  **Commit your changes** using a clear and descriptive commit message.
9.  **Push your branch** to your fork on GitHub.
10. **Open a pull request** to the `main` branch of the `juanfkurucz/book-reader` repository.
11. Fill out the pull request template, linking to any relevant issues.
12. Ensure all status checks pass. Address any feedback from maintainers.

## Style Guides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature").
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...").
- Limit the first line to 72 characters or less.
- Reference issues and pull requests liberally after the first line.

### Python Styleguide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/).
- Use `ruff format` (which is similar to Black) for code formatting.
- Use `ruff check` for linting.
- Add type hints and ensure `mypy` passes.

Thank you for your contribution!
