# Stage 1: Build and install dependencies
FROM python:3.13-slim AS builder

# Prevent Python from writing pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv
RUN python -m pip install --upgrade pip uv

# Copy project definition and source code
COPY pyproject.toml pyproject.toml
COPY src/ /app/src/

# Install the project and all dependencies into system site-packages
# uv install handles building wheels if needed
RUN uv pip install --system --no-cache .

# Stage 2: Final image
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-root user and group first
# Run as root to install packages and set up environment
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup --no-create-home appuser

# Copy installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
# Copy potentially installed executables (like the book-reader command itself)
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Create directories needed by the application and set ownership
# Doing this before switching user
ENV BOOKS_DIR=/app/books
ENV AUDIOBOOKS_DIR=/app/audiobooks
RUN mkdir -p $BOOKS_DIR $AUDIOBOOKS_DIR && \
    chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Set the entrypoint to run the installed module
ENTRYPOINT ["python", "-m", "book_reader"]

# Default command (e.g., show help)
CMD ["--help"]
