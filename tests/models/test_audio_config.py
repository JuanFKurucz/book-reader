"""Tests for the AudioConfig model."""

import pytest

from book_reader.models.audio_config import AudioConfig, TTSModel, TTSVoice


class TestAudioConfig:
    """Tests for the AudioConfig class."""

    def test_default_initialization(self) -> None:
        """Test default initialization of AudioConfig."""
        config = AudioConfig()
        assert config.model == TTSModel.STANDARD
        assert config.voice == TTSVoice.SHIMMER
        assert config.max_text_length == 4096

    @pytest.mark.parametrize(
        "voice_enum",
        [
            TTSVoice.ALLOY,
            TTSVoice.ASH,
            TTSVoice.BALLAD,
            TTSVoice.CORAL,
            TTSVoice.ECHO,
            TTSVoice.FABLE,
            TTSVoice.NOVA,
            TTSVoice.ONYX,
            TTSVoice.SAGE,
            TTSVoice.SHIMMER,
        ],
    )
    def test_valid_voices_enum(self, voice_enum: TTSVoice) -> None:
        """Test that valid voice Enums are accepted."""
        config = AudioConfig(voice=voice_enum)
        assert config.voice == voice_enum

    @pytest.mark.parametrize(
        "model_enum",
        [
            TTSModel.STANDARD,
            TTSModel.HIGH_QUALITY,
            TTSModel.GPT4O_MINI,
        ],
    )
    def test_valid_models_enum(self, model_enum: TTSModel) -> None:
        """Test that valid model Enums are accepted."""
        config = AudioConfig(model=model_enum)
        assert config.model == model_enum

    def test_max_text_length(self) -> None:
        """Test setting max_text_length."""
        config = AudioConfig(max_text_length=1000)
        assert config.max_text_length == 1000

    def test_from_strings_valid(self) -> None:
        """Test creating AudioConfig from valid strings."""
        config = AudioConfig.from_strings(model_str="tts-1-hd", voice_str="alloy")
        assert config.model == TTSModel.HIGH_QUALITY
        assert config.voice == TTSVoice.ALLOY

    def test_from_strings_invalid_fallback(self) -> None:
        """Test from_strings falls back to defaults for invalid strings."""
        config = AudioConfig.from_strings(model_str="invalid", voice_str="invalid")
        assert config.model == TTSModel.STANDARD  # Default
        assert config.voice == TTSVoice.SHIMMER  # Default
