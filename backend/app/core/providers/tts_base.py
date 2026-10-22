from abc import ABC, abstractmethod
from typing import Optional

class BaseTTSProvider(ABC):
    """
    Abstract Base Class for Voice/Audio generation.
    Enables swapping between Google Cloud Neural2, Edge-TTS, ElevenLabs, or Mock providers.
    """

    @abstractmethod
    async def synthesize_scene_audio(
        self,
        script: str,
        output_filepath: str,
        voice_id: Optional[str] = None,
    ) -> float:
        """
        Synthesize spoken script into an audio file (.mp3 / .wav).
        Returns the exact audio duration in seconds.
        """
        pass
