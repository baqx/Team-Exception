from app.config import settings
from app.core.providers.ai_base import BaseAIProvider
from app.core.providers.tts_base import BaseTTSProvider
from app.core.providers.storage_base import BaseStorageProvider

from app.services.ai.gemini_provider import GeminiProvider
from app.services.ai.mock_provider import MockAIProvider
from app.services.tts.edge_tts_provider import EdgeTTSProvider
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

def get_tts_provider() -> BaseTTSProvider:
    """Factory to instantiate configured TTS voice engine."""
    provider_name = settings.TTS_PROVIDER.lower().strip()
    if provider_name == "edge":
        return EdgeTTSProvider()
    else:
        # Default to Edge-TTS for robust local and cloud support
        return EdgeTTSProvider()

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
