# Installation Guide

This guide provides instructions for installing and setting up Book Reader on your system.

## Prerequisites

Before installing Book Reader, ensure you have the following:

- Python 3.13.3 or higher
- pip (Python package installer)
- An OpenAI API key with access to the TTS API

## Installation Methods

Book Reader can be installed in several ways:

1. Using pip (recommended for most users)
2. From source (for developers or latest features)
3. Using Docker (for containerized deployment)

## Using pip

The simplest way to install Book Reader is via pip:

```bash
pip install book-reader
```

To install a specific version:

```bash
pip install book-reader==1.2.0
```

To upgrade to the latest version:

```bash
pip install --upgrade book-reader
```

## From Source

For the latest development version or to contribute to Book Reader:

```bash
# Clone the repository
git clone https://github.com/juanfkurucz/book-reader.git
cd book-reader

# Install in development mode
pip install -e .
```

This creates an editable installation, where changes to the source code will be immediately available without reinstalling.

## Using Docker

Book Reader is available as a Docker image, which is useful for isolated environments or deployment:

```bash
# Pull the latest image
docker pull juanfkurucz/book-reader:latest

# Test the installation
docker run --rm juanfkurucz/book-reader:latest --help
```

## Verifying Installation

After installation, verify that Book Reader is correctly installed:

```bash
book-reader --version
```

You should see the current version number of Book Reader displayed.

## Setting Up Your API Key

Book Reader requires an OpenAI API key to function. You can set it in several ways:

1. **Environment variable** (recommended):
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

2. **Configuration file**:
   Create a `config.yaml` file in your home directory or current working directory:
   ```yaml
   openai_api_key: "your-api-key-here"
   ```

3. **Command line** (not recommended for security reasons):
   ```bash
   book-reader --api-key "your-api-key-here" convert document.pdf
   ```

## Installation Options

### Virtual Environment

It's recommended to install Book Reader within a virtual environment to avoid dependency conflicts:

```bash
# Create a virtual environment
python -m venv book-reader-env

# Activate the virtual environment
# On Windows:
book-reader-env\Scripts\activate
# On macOS/Linux:
source book-reader-env/bin/activate

# Install Book Reader
pip install book-reader
```

### Installing Optional Dependencies

Book Reader has optional dependencies for enhanced functionality:

```bash
# Install with all optional dependencies
pip install book-reader[all]

# Install with specific optional dependencies
pip install book-reader[dev]  # Development tools
pip install book-reader[test]  # Testing tools
```

## Troubleshooting

### Common Installation Issues

1. **Dependency Conflicts**:
   ```bash
   pip install --upgrade pip
   pip install book-reader --force-reinstall
   ```

2. **Permission Issues**:
   ```bash
   pip install --user book-reader
   ```

3. **OpenAI API Key Not Found**:
   Ensure your API key is correctly set as an environment variable or in the configuration file.

4. **Module Not Found Errors**:
   ```bash
   pip install book-reader[all]
   ```

5. **Docker Permission Issues**:
   ```bash
   # On Linux, if you get permission errors:
   sudo docker pull juanfkurucz/book-reader:latest
   sudo docker run --rm juanfkurucz/book-reader:latest --help
   ```

### Getting Help

If you encounter issues not covered here:

- Check the [GitHub Issues](https://github.com/juanfkurucz/book-reader/issues) for similar problems
- Create a new issue with details about your problem
- Join our community Discord for real-time help

## Next Steps

After installation:

1. Set up your configuration file following the [Configuration Guide](configuration.md)
2. Try converting your first PDF to audiobook following the [Usage Guide](usage.md)
3. Explore the [API Documentation](api.md) if you're a developer

## Upgrading

To upgrade Book Reader to the latest version:

```bash
pip install --upgrade book-reader
```

For Docker:

```bash
docker pull juanfkurucz/book-reader:latest
```

## Uninstallation

If you need to uninstall Book Reader:

```bash
pip uninstall book-reader
```

For Docker, you can remove the image:

```bash
docker rmi juanfkurucz/book-reader:latest
```
