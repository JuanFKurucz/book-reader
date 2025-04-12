# Contributing to Book Reader

Thank you for your interest in contributing to Book Reader! This document provides guidelines and instructions for contributing to the project.

## Getting Started

1. **Fork the repository**: Start by forking the [Book Reader repository](https://github.com/juanfkurucz/book-reader) on GitHub.

2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/book-reader.git
   cd book-reader
   ```

3. **Set up the development environment**:
   ```bash
   # Create a virtual environment
   python -m venv venv

   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate

   # Install dependencies
   pip install -e ".[dev]"
   ```

## Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**: Implement your feature or bug fix.

3. **Run tests**: Ensure your changes pass all tests.
   ```bash
   pytest
   ```

4. **Check code quality**: Run the linters to ensure your code follows our style guidelines.
   ```bash
   flake8
   ```

5. **Commit your changes**:
   ```bash
   git commit -m "Description of your changes"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a pull request**: Submit a pull request from your forked repository to the main Book Reader repository.

## Code Guidelines

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Write docstrings for all functions, classes, and methods
- Add type annotations to function signatures
- Keep lines under 79 characters
- Use meaningful variable and function names

## Adding Features

If you're adding a new feature:

1. Start by opening an issue describing the feature
2. Write tests for your feature
3. Implement your feature
4. Update the documentation

## Documentation

When adding or changing features, please update the corresponding documentation:

1. Update or add docstrings
2. Update the relevant files in the `docs/` directory
3. If you've added new commands or options, update the usage guide

To view your documentation changes locally:
```bash
mkdocs serve
```

Then visit `http://127.0.0.1:8000` in your browser.

## Testing

- Write unit tests for new functionality
- Make sure existing tests continue to pass
- Integration tests should be added for significant features

## Pull Request Process

1. Update the README.md or documentation with details of changes if appropriate
2. Update the CHANGELOG.md with a description of your changes
3. The PR should work on the main branch and pass all CI checks
4. The PR will be merged once it receives approval from maintainers

## Community

- Be respectful and inclusive in your communications
- Help others who have questions
- Share your ideas and feedback

## License

By contributing to Book Reader, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
