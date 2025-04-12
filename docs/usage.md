# Usage Guide

This guide explains how to use Book Reader to convert PDF documents to audiobooks.

## Basic Commands

### Converting a PDF to Audio

To convert a PDF document to an audiobook:

```bash
book-reader convert path/to/your/document.pdf
```

By default, this will create audio files in a directory named after your PDF in the current working directory.

### Specifying an Output Directory

To specify where the audio files should be saved:

```bash
book-reader convert path/to/your/document.pdf --output-dir /path/to/output
```

### Setting Audio Quality and Voice

You can customize the text-to-speech conversion:

```bash
book-reader convert path/to/your/document.pdf --voice nova --model tts-1-hd
```

Available voices include:
- `alloy`
- `echo`
- `fable`
- `nova` (default)
- `onyx`
- `shimmer`

Models include:
- `tts-1` (default, faster processing)
- `tts-1-hd` (higher quality audio)

### Setting Playback Speed

Adjust the speaking speed:

```bash
book-reader convert path/to/your/document.pdf --speed 1.2
```

Values range from 0.5 (slower) to 2.0 (faster), with 1.0 being the default.

## Advanced Usage

### Processing Specific Pages

To process only specific pages:

```bash
book-reader convert path/to/your/document.pdf --pages 10-20
```

### Resuming a Conversion

If a conversion was interrupted, you can resume from where it left off:

```bash
book-reader convert path/to/your/document.pdf --resume
```

### Batch Processing

Control how many pages are processed in a single batch:

```bash
book-reader convert path/to/your/document.pdf --batch-size 10
```

### Concurrent Processing

Control the number of parallel processing tasks:

```bash
book-reader convert path/to/your/document.pdf --concurrent-tasks 4
```

### Combining Multiple Options

You can combine multiple options:

```bash
book-reader convert path/to/your/document.pdf \
  --output-dir ~/audiobooks/my-book \
  --voice onyx \
  --model tts-1-hd \
  --speed 1.1 \
  --batch-size 15 \
  --concurrent-tasks 3
```

## Using with Docker

If you're using the Docker image:

```bash
docker run --rm \
  -v $(pwd)/my-pdfs:/pdfs \
  -v $(pwd)/my-output:/output \
  -e OPENAI_API_KEY="your-api-key-here" \
  juanfkurucz/book-reader:latest \
  convert /pdfs/document.pdf --output-dir /output
```

## Configuration File

Instead of specifying options on the command line, you can create a configuration file. Book Reader looks for `config.yaml` in these locations:

1. Current working directory
2. User's home directory in `~/.config/book-reader/config.yaml`

Example `config.yaml`:

```yaml
# Default conversion settings
default_output_dir: "~/audiobooks"
batch_size: 15
concurrent_tasks: 2

# Audio settings
audio:
  voice: "nova"
  model: "tts-1"
  speed: 1.0
  format: "mp3"

# API settings
openai_api_key: "your-api-key-here"
```

## Viewing Conversion Progress

The conversion progress is displayed in real-time on the command line:

```
Converting "mybook.pdf" to audiobook...
Pages: 6/120 [===>                   ] 5% | ETA: 55m20s
```

## Managing Existing Conversions

### List Converted Books

To see all previously converted books:

```bash
book-reader list
```

### Getting Book Information

To get detailed information about a specific conversion:

```bash
book-reader info path/to/output/directory
```

## Troubleshooting

### Logging

To enable verbose logging for debugging:

```bash
book-reader convert path/to/document.pdf --verbose
```

For even more detailed logs:

```bash
book-reader convert path/to/document.pdf --log-level debug
```

### Common Issues

- **API Key Issues**: Ensure your OpenAI API key is set correctly and has access to the TTS API.
- **Memory Issues**: If you encounter memory errors, try reducing the `batch_size` and `concurrent_tasks` values.
- **PDF Reading Issues**: Some PDFs with complex formatting may not convert properly. Try extracting the text to a plain text file first if possible.
- **Unicode or Special Character Issues**: If your PDF contains special characters that don't convert properly, try using the `--preprocessing` flag to apply text cleanup.

## Examples

### Converting a Technical Book with High Quality

```bash
book-reader convert programming_book.pdf \
  --model tts-1-hd \
  --voice onyx \
  --speed 0.9 \
  --output-dir ~/audiobooks/programming
```

### Quick Conversion of a Novel

```bash
book-reader convert novel.pdf \
  --model tts-1 \
  --voice nova \
  --speed 1.1
```

### Converting a Large Document in Sections

```bash
# Process the first 50 pages
book-reader convert large_document.pdf --pages 1-50

# Process the next 50 pages
book-reader convert large_document.pdf --pages 51-100

# Process the final 50 pages
book-reader convert large_document.pdf --pages 101-150
```

### Using a Configuration File with Command Overrides

Create a `config.yaml` with your preferred defaults, then override specific settings as needed:

```bash
book-reader convert document.pdf --voice shimmer
```

This uses all other settings from your configuration file but changes the voice to "shimmer".

## Command Reference

### Main Commands

| Command | Description |
|---------|-------------|
| `convert` | Convert a PDF to audiobook |
| `list` | List all converted books |
| `info` | Show details about a conversion |
| `config` | Manage configuration settings |
| `version` | Show version information |
| `help` | Show help for commands |

### Convert Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output-dir` | Directory to save audio files | Current directory |
| `--voice` | Voice for TTS | "nova" |
| `--model` | TTS model | "tts-1" |
| `--speed` | Playback speed | 1.0 |
| `--batch-size` | Pages per batch | 15 |
| `--concurrent-tasks` | Parallel processes | 2 |
| `--resume` | Resume interrupted conversion | False |
| `--pages` | Page range to process | All pages |
| `--verbose` | Enable verbose logging | False |
| `--log-level` | Set logging level | "info" |
| `--no-progress` | Disable progress bar | False |
| `--format` | Audio format | "mp3" |

## Best Practices

1. **Begin with a small batch**: Try converting a few pages first to verify voice/quality before processing a large document.
2. **Use appropriate batching**: For large books, use appropriate batching to avoid memory issues.
3. **Secure your API key**: Never commit your API key to version control or share it publicly.
4. **Configure for your use case**: Technical books may benefit from slower speeds, while fiction might be enjoyable at normal or faster speeds.
5. **Enable resumption**: When converting large documents, always use the `--resume` flag to handle potential interruptions.
