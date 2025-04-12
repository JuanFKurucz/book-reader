# Configuration Guide

Book Reader offers several ways to configure its behavior to suit your needs. This guide explains all available configuration options and methods.

## Configuration Methods

Book Reader uses a cascading priority system for configuration:

1. **Command-line arguments** (highest priority)
2. **Environment variables**
3. **Configuration file**
4. **Default values** (lowest priority)

## Configuration File

Book Reader looks for a `config.yaml` file in these locations (in order):

1. Current working directory
2. User's home directory (`~/.config/book-reader/config.yaml`)

### Example Configuration File

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

# Logging and display
log_level: "info"
disable_progress_bar: false
```

## Environment Variables

You can configure Book Reader using environment variables:

| Environment Variable | Description |
|----------------------|-------------|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `BOOK_READER_VOICE` | Default voice for TTS |
| `BOOK_READER_MODEL` | Default TTS model |
| `BOOK_READER_BATCH_SIZE` | Default batch size |
| `BOOK_READER_OUTPUT_DIR` | Default output directory |
| `BOOK_READER_CONCURRENT_TASKS` | Default number of concurrent tasks |
| `BOOK_READER_LOG_LEVEL` | Logging level (debug, info, warning, error) |
| `BOOK_READER_DISABLE_PROGRESS` | Set to "true" to disable progress bar |

## Command-Line Arguments

Command-line arguments always take precedence over other configuration methods:

```bash
book-reader convert document.pdf \
  --output-dir ~/audiobooks/my-book \
  --voice nova \
  --model tts-1-hd \
  --speed 1.1 \
  --batch-size 15 \
  --concurrent-tasks 3 \
  --verbose
```

## Configuration Options

### General Options

| Option | Description | Default | Environment Variable |
|--------|-------------|---------|---------------------|
| `output-dir` | Directory to save audio files | Current directory | `BOOK_READER_OUTPUT_DIR` |
| `batch-size` | Number of PDF pages to process in a batch | 15 | `BOOK_READER_BATCH_SIZE` |
| `concurrent-tasks` | Number of concurrent TTS tasks | 2 | `BOOK_READER_CONCURRENT_TASKS` |
| `resume` | Resume from last processed page | False | - |
| `pages` | Range of pages to process (e.g., "5-10") | All pages | - |
| `verbose` | Enable verbose logging | False | - |
| `config` | Path to config file | - | - |

### Audio Options

| Option | Description | Default | Environment Variable |
|--------|-------------|---------|---------------------|
| `voice` | Voice to use for TTS | "nova" | `BOOK_READER_VOICE` |
| `model` | TTS model to use | "tts-1" | `BOOK_READER_MODEL` |
| `speed` | Speed factor for audio playback | 1.0 | `BOOK_READER_SPEED` |
| `format` | Audio format (mp3, wav) | "mp3" | `BOOK_READER_FORMAT` |

### Available Voices

OpenAI's TTS API offers several voice options:

| Voice | Description |
|-------|-------------|
| `alloy` | Neutral voice with balanced tone |
| `echo` | Versatile voice with clear, assertive delivery |
| `fable` | Expressive voice with a warmer tone |
| `nova` | Gentle and calm voice (default) |
| `onyx` | Deep and authoritative voice |
| `shimmer` | Light, conversational tone |

### Available Models

| Model | Description |
|-------|-------------|
| `tts-1` | Standard quality, faster processing (default) |
| `tts-1-hd` | Higher audio quality, larger file size |

## Advanced Configuration

### Logging Configuration

You can control the logging verbosity:

```yaml
# In config.yaml
log_level: "debug"  # Options: debug, info, warning, error
log_file: "~/book-reader.log"  # Optional: Log to file
```

Or via environment variable:

```bash
export BOOK_READER_LOG_LEVEL=debug
```

Or via command line:

```bash
book-reader convert document.pdf --verbose  # Increases log level
```

### Progress Bar Configuration

You can disable the progress bar:

```yaml
# In config.yaml
disable_progress_bar: true
```

Or via environment variable:

```bash
export BOOK_READER_DISABLE_PROGRESS=true
```

Or via command line:

```bash
book-reader convert document.pdf --no-progress
```

### API Configuration

Book Reader requires an OpenAI API key with access to the TTS API:

```yaml
# In config.yaml
openai_api_key: "your-api-key-here"
```

Or via environment variable (recommended):

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Configuration for Docker

When using Docker, you can pass environment variables and mount a configuration file:

```bash
docker run --rm \
  -v $(pwd)/my-pdfs:/pdfs \
  -v $(pwd)/my-output:/output \
  -v $(pwd)/config.yaml:/app/config.yaml \
  -e OPENAI_API_KEY="your-api-key-here" \
  -e BOOK_READER_CONCURRENT_TASKS=4 \
  juanfkurucz/book-reader:latest \
  convert /pdfs/document.pdf --output-dir /output
```

## Configuration Precedence Example

If you set the same option in multiple places, here's how precedence works:

1. Command-line: `--voice echo`
2. Environment variable: `BOOK_READER_VOICE=nova`
3. Config file: `audio: { voice: "alloy" }`
4. Default value: `"nova"`

In this example, `echo` would be used because command-line arguments have the highest priority.

## Tips for Configuration

1. **Use a config file** for settings that remain constant between runs
2. **Use environment variables** for sensitive information like API keys
3. **Use command-line arguments** for one-off changes or specific conversion needs
4. **Start with default values** and adjust based on your experience

## Debugging Configuration

To see what configuration is being used:

```bash
book-reader config show
```

This displays the effective configuration after merging all sources.
