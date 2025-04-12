"""Audio Configuration model."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class TTSModel(Enum):
    """Text-to-Speech model options."""

    STANDARD = "tts-1"
    HIGH_QUALITY = "tts-1-hd"
    GPT4O_MINI = "gpt-4o-mini-tts"


class TTSVoice(Enum):
    """Text-to-Speech voice options."""

    ALLOY = "alloy"
    ASH = "ash"
    BALLAD = "ballad"
    CORAL = "coral"
    ECHO = "echo"
    FABLE = "fable"
    NOVA = "nova"
    ONYX = "onyx"
    SAGE = "sage"
    SHIMMER = "shimmer"


@dataclass
class AudioConfig:
    """Audio configuration options."""

    model: TTSModel = TTSModel.STANDARD
    voice: TTSVoice = TTSVoice.SHIMMER
    output_dir: Path = Path("./audiobooks")
    max_text_length: int = 4096
    sample_rate: int = 22050

    @classmethod
    def from_strings(
        cls,
        model_str: str = "tts-1",
        voice_str: str = "shimmer",
        output_dir: Optional[str] = None,
    ) -> "AudioConfig":
        """Create AudioConfig from string values."""
        # Find matching model
        model = TTSModel.STANDARD
        for m in TTSModel:
            if m.value == model_str:
                model = m
                break

        # Find matching voice
        voice = TTSVoice.SHIMMER
        for v in TTSVoice:
            if v.value == voice_str:
                voice = v
                break

        # Create config
        config = cls(model=model, voice=voice)

        # Set output dir if provided
        if output_dir:
            config.output_dir = Path(output_dir)

        return config
