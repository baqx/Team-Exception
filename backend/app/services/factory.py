from typing import Optional
from app.config import settings
from app.core.providers.ai_base import BaseAIProvider
from app.core.providers.tts_base import BaseTTSProvider
from app.core.providers.storage_base import BaseStorageProvider

from app.services.ai.gemini_provider import GeminiProvider
from app.services.ai.mock_provider import MockAIProvider
from app.services.tts.edge_tts_provider import EdgeTTSProvider
from app.services.tts.yarngpt_provider import YarnGPTProvider
from app.services.storage.local_storage import LocalStorageProvider
from app.services.storage.cloudinary_storage import CloudinaryStorageProvider

def get_ai_provider() -> BaseAIProvider:
    """Factory to instantiate configured AI provider."""
    provider_name = settings.AI_PROVIDER.lower().strip()
    if provider_name == "gemini":
        # Fallback to mock if API key isn't provided yet
        if not settings.GOOGLE_GENERATIVE_AI_API_KEY:
            return MockAIProvider()
        return GeminiProvider()
    elif provider_name == "mock":
        return MockAIProvider()
    else:
        raise ValueError(f"Unsupported AI_PROVIDER: {provider_name}. Choose 'gemini' or 'mock'.")

class SmartTTSProvider(BaseTTSProvider):
    """
    Intelligent dispatching TTS provider.
    Inspects voice_id at runtime:
      - 'yarngpt:*' or known YarnGPT voice names -> YarnGPTProvider
      - 'edge:*' or empty -> EdgeTTSProvider (Christopher)
    """
    def __init__(self):
        self.edge_provider = EdgeTTSProvider()
        self.yarngpt_provider = YarnGPTProvider()

    async def synthesize_scene_audio(
        self,
        script: str,
        output_filepath: str,
        voice_id: Optional[str] = None,
    ) -> float:
        vid = (voice_id or "").strip()
        clean_name = vid.lower()
        if clean_name.startswith("yarngpt:"):
            clean_name = clean_name[len("yarngpt:"):]

        if vid.lower().startswith("yarngpt:") or clean_name in YarnGPTProvider.KNOWN_VOICES:
            return await self.yarngpt_provider.synthesize_scene_audio(
                script=script,
                output_filepath=output_filepath,
                voice_id=clean_name,
            )
        else:
            edge_voice = vid.replace("edge:", "") if vid.startswith("edge:") else vid
            return await self.edge_provider.synthesize_scene_audio(
                script=script,
                output_filepath=output_filepath,
                voice_id=edge_voice or settings.EDGE_TTS_VOICE,
            )

def get_tts_provider() -> BaseTTSProvider:
    """Factory to instantiate configured TTS voice engine."""
    provider_name = settings.TTS_PROVIDER.lower().strip()
    if provider_name == "yarngpt":
        return YarnGPTProvider()
    elif provider_name == "edge":
        return SmartTTSProvider()
    else:
        return SmartTTSProvider()

def get_storage_provider() -> BaseStorageProvider:
    """Factory to instantiate configured video storage / CDN provider."""
    provider_name = settings.STORAGE_PROVIDER.lower().strip()
    if provider_name == "cloudinary":
        if not settings.CLOUDINARY_CLOUD_NAME:
            return LocalStorageProvider()
        return CloudinaryStorageProvider()
    elif provider_name == "local":
        return LocalStorageProvider()
    else:
        return LocalStorageProvider()
