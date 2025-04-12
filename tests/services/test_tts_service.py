"""Tests for the TTSService implementations."""

import os
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock, mock_open, patch

import pytest

from book_reader.models.audio_config import AudioConfig
from book_reader.services.tts_service import (
    OpenAILegacyTTSService,
    OpenAIModernTTSService,
    OpenAIRESTTTSService,
    OpenAITTSServiceFactory,
)


@pytest.fixture
def audio_config() -> AudioConfig:
    """Create a default AudioConfig instance."""
    return AudioConfig()


@pytest.fixture
def mock_openai_client_instance() -> MagicMock:
    """Mock the OpenAI client object instance."""
    mock_client = MagicMock()
    mock_speech_response = MagicMock()
    mock_client.audio.speech.create.return_value = mock_speech_response
    return mock_client


@pytest.fixture
def mock_openai_class(
    mock_openai_client_instance: MagicMock,
) -> Generator[MagicMock, None, None]:
    with patch("openai.OpenAI") as mock_class:
        mock_class.return_value = mock_openai_client_instance
        yield mock_class


@pytest.fixture
def mock_requests_post() -> MagicMock:
    """Create a mock for requests.post."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"fake audio content"
    return mock_response


class TestOpenAILegacyTTSService:
    """Tests for the OpenAILegacyTTSService."""

    @pytest.fixture
    def service(self, mock_requests_post: MagicMock) -> OpenAILegacyTTSService:
        """Create an OpenAILegacyTTSService instance with mocked API key."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
            return OpenAILegacyTTSService()

    def test_legacy_init_no_key(self) -> None:
        """Test initialization raises ValueError if API key is missing."""
        with patch.dict(os.environ, {}, clear=True):
            # Ensure key is not present
            with pytest.raises(ValueError, match="OPENAI_API_KEY not found"):
                OpenAILegacyTTSService()

    def test_legacy_synthesize_success(
        self,
        service: OpenAILegacyTTSService,
        audio_config: AudioConfig,
        tmp_path: Path,
        mock_requests_post: MagicMock,
    ) -> None:
        """Test successful synthesize call with legacy API."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"audio_data"
        output_path = tmp_path / "audio"

        with patch("requests.post", return_value=mock_response) as mock_post:
            with patch("builtins.open", mock_open()) as mocked_file:
                result_path = service.synthesize(
                    "Test text", output_path, 0, audio_config
                )

                mock_post.assert_called_once_with(
                    "https://api.openai.com/v1/audio/speech",
                    headers={
                        "Authorization": "Bearer test_key",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": audio_config.model.value,
                        "voice": audio_config.voice.value,
                        "input": "Test text",
                    },
                )
                mocked_file.assert_called_once_with(output_path / "chunk_001.mp3", "wb")
                mocked_file().write.assert_called_once_with(b"audio_data")
                assert result_path == output_path / "chunk_001.mp3"

    def test_legacy_synthesize_api_error(
        self,
        service: OpenAILegacyTTSService,
        audio_config: AudioConfig,
        tmp_path: Path,
        mock_requests_post: MagicMock,
    ) -> None:
        """Test synthesize with legacy API error."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"

        with patch("requests.post", return_value=mock_response):
            with pytest.raises(Exception, match="API Error: 400"):
                service.synthesize("Test text", tmp_path / "audio", 0, audio_config)


class TestOpenAIModernTTSService:
    """Tests for the OpenAIModernTTSService."""

    @pytest.fixture
    def service(self, mock_openai_class: MagicMock) -> OpenAIModernTTSService:
        """Create an OpenAIModernTTSService instance."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
            return OpenAIModernTTSService()

    def test_modern_init_no_key(self, mock_openai_class: MagicMock) -> None:
        """Test initialization raises ValueError if API key is missing."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="OPENAI_API_KEY not found"):
                OpenAIModernTTSService()
        mock_openai_class.assert_not_called()

    def test_modern_synthesize_success(
        self,
        service: OpenAIModernTTSService,
        audio_config: AudioConfig,
        tmp_path: Path,
        mock_openai_client_instance: MagicMock,
    ) -> None:
        """Test successful synthesize call with modern API."""
        output_path = tmp_path / "audio_modern"
        expected_path = output_path / "chunk_001.mp3"

        result_path = service.synthesize("test text", output_path, 0, audio_config)

        assert result_path == expected_path
        mock_openai_client_instance.audio.speech.create.assert_called_once_with(
            model=audio_config.model.value,
            voice=audio_config.voice.value,
            input="test text",
        )
        mock_speech_response = (
            mock_openai_client_instance.audio.speech.create.return_value
        )
        mock_speech_response.stream_to_file.assert_called_once_with(str(expected_path))

    def test_modern_synthesize_api_error(
        self,
        service: OpenAIModernTTSService,
        audio_config: AudioConfig,
        tmp_path: Path,
        mock_openai_client_instance: MagicMock,
    ) -> None:
        """Test synthesize with modern API error."""
        mock_openai_client_instance.audio.speech.create.side_effect = Exception(
            "API Error"
        )
        output_path = tmp_path / "audio_modern_error"
        with pytest.raises(Exception, match="API Error"):
            service.synthesize("test text", output_path, 0, audio_config)


class TestOpenAIRESTTTSService:
    """Tests for the OpenAIRESTTTSService."""

    @pytest.fixture
    def service(self) -> OpenAIRESTTTSService:
        """Create an OpenAIRESTTTSService instance."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
            return OpenAIRESTTTSService()

    def test_rest_init_no_key(self) -> None:
        """Test initialization raises ValueError if API key is missing."""
        with patch.dict(os.environ, {}, clear=True):
            # Ensure key is not present
            with pytest.raises(ValueError, match="OPENAI_API_KEY not found"):
                OpenAIRESTTTSService()

    def test_rest_synthesize_success(
        self,
        service: OpenAIRESTTTSService,
        audio_config: AudioConfig,
        tmp_path: Path,
        mock_requests_post: MagicMock,
    ) -> None:
        """Test successful synthesize call with REST API."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"audio_data"
        output_path = Path("./test_audio")

        with patch("requests.post", return_value=mock_response) as mock_post:
            with patch("builtins.open", mock_open()) as mocked_file:
                result_path = service.synthesize(
                    "Test text", output_path, 0, audio_config
                )

                mock_post.assert_called_once_with(
                    "https://api.openai.com/v1/audio/speech",
                    headers={
                        "Authorization": "Bearer test_key",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": audio_config.model.value,
                        "voice": audio_config.voice.value,
                        "input": "Test text",
                    },
                )
                mocked_file.assert_called_once_with(output_path / "chunk_001.mp3", "wb")
                mocked_file().write.assert_called_once_with(b"audio_data")
                assert result_path == output_path / "chunk_001.mp3"

    def test_rest_synthesize_api_error(
        self,
        service: OpenAIRESTTTSService,
        audio_config: AudioConfig,
        tmp_path: Path,
        mock_requests_post: MagicMock,
    ) -> None:
        """Test synthesize with REST API error."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"

        with patch("requests.post", return_value=mock_response):
            with pytest.raises(Exception, match="API Error: 400"):
                service.synthesize("Test text", Path("./test_audio"), 0, audio_config)


class TestOpenAITTSServiceFactory:
    """Tests for the OpenAITTSServiceFactory."""

    @patch("openai.__version__", "0.28.0")  # Test legacy detection
    def test_create_legacy_service(self) -> None:
        """Test creating a legacy service."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
            service = OpenAITTSServiceFactory.create()
            assert isinstance(service, OpenAILegacyTTSService)

    @patch("openai.__version__", "1.1.0")  # Test modern detection
    @patch("book_reader.services.tts_service.OpenAIModernTTSService")
    def test_create_modern_service(self, mock_modern_service: MagicMock) -> None:
        """Test creating a modern service."""
        mock_modern_service.return_value = MagicMock()
        service = OpenAITTSServiceFactory.create()
        assert service == mock_modern_service.return_value
        mock_modern_service.assert_called_once()

    @patch("openai.__version__", "1.1.0")  # Test modern detection
    @patch(
        "book_reader.services.tts_service.OpenAIModernTTSService",
        side_effect=ImportError("cannot import"),
    )
    @patch("book_reader.services.tts_service.OpenAIRESTTTSService")
    def test_create_fallback_to_rest(
        self, mock_rest_service: MagicMock, mock_modern_import: MagicMock
    ) -> None:
        """Test fallback to REST service when modern SDK fails."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
            mock_rest_service.return_value = MagicMock()
            service = OpenAITTSServiceFactory.create()
            assert service == mock_rest_service.return_value
            mock_rest_service.assert_called_once()
