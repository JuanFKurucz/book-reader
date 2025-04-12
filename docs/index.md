# Book Reader Documentation

Book Reader is a command-line utility that converts PDF books into audiobooks using OpenAI's text-to-speech service. It handles the extraction of text from PDF files and generates high-quality audio files.

## Features

- Convert PDF files to audiobooks with OpenAI's text-to-speech service
- Resume conversion from where you left off
- Process PDFs in batches to manage large books
- Control voice type and audio quality
- Concurrent processing for faster conversion
- Docker support for easy deployment

## Requirements

- Python 3.13.3 or higher
- An OpenAI API key with access to the TTS API

## Getting Started

- [Installation Guide](installation.md): Learn how to install Book Reader
- [Usage Guide](usage.md): Discover how to use Book Reader effectively
- [Configuration Guide](configuration.md): Customize Book Reader to your needs

## Documentation

This documentation is automatically deployed to GitHub Pages whenever changes are pushed to the main branch. You can access the latest version at:

[https://juanfkurucz.github.io/book-reader/](https://juanfkurucz.github.io/book-reader/)

## How It Works

Book Reader works by:

1. Reading the PDF file and extracting text content
2. Processing the text to optimize for text-to-speech conversion
3. Sending the processed text to OpenAI's TTS API
4. Saving the resulting audio files to your specified output directory

For large PDFs, Book Reader processes pages in batches and can resume from where it left off if the conversion is interrupted.

## Acknowledgements

Book Reader was inspired by and built upon the valuable work of the following projects and developers:

- [epub-to-audiobook](https://github.com/fairy-root/epub-to-audiobook) by [fairy-root](https://github.com/fairy-root) - A Python script that converts EPUB books to audiobooks using OpenAI's TTS API
- [bulletReader](https://github.com/facundop3/bulletReader) by [facundop3](https://github.com/facundop3) - An Electron tool designed to increase reading speed

We extend our sincere gratitude to these developers for their contributions to the open-source community and for inspiring features and approaches in Book Reader.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue on our [GitHub repository](https://github.com/juanfkurucz/book-reader).

# Book Reader

Convert PDF files to audiobooks using OpenAI TTS with multiple voice and model options.

## Overview

Book Reader is a Python CLI tool that allows you to convert PDF documents into high-quality audiobooks using OpenAI's Text-to-Speech (TTS) service. It offers a range of voices and model options to customize your listening experience.

## Features

- Convert PDF documents to audiobook audio files
- Support for multiple OpenAI voices (Alloy, Echo, Fable, Onyx, Nova, and more)
- Configurable audio quality settings
- Resume capability for interrupted conversions
- Parallel processing for faster conversions
- Progress tracking

## Quick Start

```bash
# Install the package
pip install book-reader

# Convert a PDF to audiobook with default settings
book-reader convert path/to/your/document.pdf

# Use a specific voice
book-reader convert path/to/your/document.pdf --voice nova

# Use high quality audio
book-reader convert path/to/your/document.pdf --model high-quality
```

For more detailed usage instructions, see the [Usage](usage.md) section.

# Welcome to MkDocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
