"""Text-to-Speech Service."""

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

import openai
import requests

from book_reader.models.audio_config import (
    AudioConfig,
)


class TTSService(ABC):
    """Abstract base class for Text-to-Speech services."""

    @abstractmethod
    def synthesize(
        self,
        text: str,
        output_path: Path,
        chunk_index: int,
        config: Optional[AudioConfig] = None,
    ) -> Path:
        """Convert text to speech.

        Args:
            text: Text to convert to speech
            output_path: Directory to save the audio file
            chunk_index: Index of the current chunk
            config: Audio configuration

        Returns:
            Path to the generated audio file
        """
        pass


class OpenAITTSServiceFactory:
    """Factory for creating OpenAI TTS services based on the API version."""

    @staticmethod
    def create() -> TTSService:
        """Create an OpenAI TTS service based on the installed API version.

        Returns:
            Appropriate OpenAI TTS service implementation
        """
        openai_version = openai.__version__
        is_legacy = openai_version.startswith("0.")

        print(f"Using OpenAI API version {openai_version}")
        print(f"Using legacy API: {is_legacy}")

        if is_legacy:
            return OpenAILegacyTTSService()
        else:
            try:
                # Try to create a modern service
                return OpenAIModernTTSService()
            except (AttributeError, ImportError):
                # Fallback to REST API service
                print("Modern OpenAI SDK detected but audio module not found.")
                print("Falling back to direct API calls.")
                return OpenAIRESTTTSService()


class OpenAILegacyTTSService(TTSService):
    """OpenAI TTS service using legacy API (v0.x)."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the service.

        Args:
            api_key: OpenAI API key
        """
        # Use provided API key or from environment
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

    def synthesize(
        self,
        text: str,
        output_path: Path,
        chunk_index: int,
        config: Optional[AudioConfig] = None,
    ) -> Path:
        """Convert text to speech using OpenAI's legacy API.

        Args:
            text: Text to convert to speech
            output_path: Directory to save the audio file
            chunk_index: Index of the current chunk
            config: Audio configuration

        Returns:
            Path to the generated audio file
        """
        _config = config or AudioConfig()
        # Create directory if it doesn't exist
        output_path.mkdir(parents=True, exist_ok=True)

        # Create the output file path
        file_path = output_path / f"chunk_{chunk_index + 1:03d}.mp3"

        # Direct REST API call for OpenAI v0.x
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": _config.model.value,
            "voice": _config.voice.value,
            "input": text,
        }

        response = requests.post(
            "https://api.openai.com/v1/audio/speech",
            headers=headers,
            json=payload,
        )

        if response.status_code != 200:
            error_message = f"API Error: {response.status_code} - {response.text}"
            raise Exception(error_message)

        with open(file_path, "wb") as f:
            f.write(response.content)

        print(f"Audio for chunk {chunk_index + 1} saved to {file_path}")
        return file_path


class OpenAIModernTTSService(TTSService):
    """OpenAI TTS service using modern API (v1.x+)."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the service.

        Args:
            api_key: OpenAI API key
        """
        # Use provided API key or from environment
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        # Initialize OpenAI client
        # Check if the OpenAI package has the OpenAI class
        try:
            # For OpenAI v1.x+
            from openai import OpenAI

            self.client = OpenAI(api_key=self.api_key)
        except (ImportError, AttributeError) as err:
            raise ImportError(
                "OpenAI modern API not available. "
                "Please upgrade to OpenAI v1.x+ or use OpenAIRESTTTSService."
            ) from err

    def synthesize(
        self,
        text: str,
        output_path: Path,
        chunk_index: int,
        config: Optional[AudioConfig] = None,
    ) -> Path:
        """Convert text to speech using OpenAI's modern API.

        Args:
            text: Text to convert to speech
            output_path: Directory to save the audio file
            chunk_index: Index of the current chunk
            config: Audio configuration

        Returns:
            Path to the generated audio file
        """
        _config = config or AudioConfig()
        # Create directory if it doesn't exist
        output_path.mkdir(parents=True, exist_ok=True)

        # Create the output file path
        file_path = output_path / f"chunk_{chunk_index + 1:03d}.mp3"

        # Use OpenAI's modern API
        response = self.client.audio.speech.create(
            model=_config.model.value,
            voice=_config.voice.value,
            input=text,
        )

        # Save the audio file
        response.stream_to_file(str(file_path))

        print(f"Audio for chunk {chunk_index + 1} saved to {file_path}")
        return file_path


class OpenAIRESTTTSService(TTSService):
    """OpenAI TTS service using REST API directly."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the service.

        Args:
            api_key: OpenAI API key
        """
        # Use provided API key or from environment
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

    def synthesize(
        self,
        text: str,
        output_path: Path,
        chunk_index: int,
        config: Optional[AudioConfig] = None,
    ) -> Path:
        """Convert text to speech using OpenAI's REST API directly.

        Args:
            text: Text to convert to speech
            output_path: Directory to save the audio file
            chunk_index: Index of the current chunk
            config: Audio configuration

        Returns:
            Path to the generated audio file
        """
        _config = config or AudioConfig()
        # Create directory if it doesn't exist
        output_path.mkdir(parents=True, exist_ok=True)

        # Create the output file path
        file_path = output_path / f"chunk_{chunk_index + 1:03d}.mp3"

        # Direct REST API call
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": _config.model.value,
            "voice": _config.voice.value,
            "input": text,
        }

        response = requests.post(
            "https://api.openai.com/v1/audio/speech",
            headers=headers,
            json=payload,
        )

        if response.status_code != 200:
            error_message = f"API Error: {response.status_code} - {response.text}"
            raise Exception(error_message)

        with open(file_path, "wb") as f:
            f.write(response.content)

        print(f"Audio for chunk {chunk_index + 1} saved to {file_path}")
        return file_path
