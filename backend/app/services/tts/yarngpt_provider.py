import os
import logging
from typing import Optional, List, Dict, Any
import httpx
from moviepy import AudioFileClip
from app.config import settings
from app.core.providers.tts_base import BaseTTSProvider
from app.services.tts.edge_tts_provider import EdgeTTSProvider

logger = logging.getLogger("yarngpt_provider")

class YarnGPTProvider(BaseTTSProvider):
    """
    African Voice AI provider powered by YarnGPT (https://yarngpt.ai).
    Produces authentic African-accented neural voices (Nigerian English, Pidgin, Yoruba, Igbo, Hausa).
    Features automated fail-safe fallback to Edge-TTS so the video render pipeline never fails.
    """

    KNOWN_VOICES = {
        "idera", "emma", "umar", "chinenye", "remi", "osagie", 
        "adaora", "mary", "zainab", "adam", "wura", "jude", 
        "tayo", "regina", "femi", "nonso"
    }

    # Curated voice catalog with rich metadata for frontend presentation
    CATALOG: List[Dict[str, Any]] = [
        {
            "id": "yarngpt:idera",
            "voice_name": "idera",
            "provider": "yarngpt",
            "display_name": "Idera",
            "description": "Melodic, gentle, and patient delivery.",
            "accent": "Nigerian English",
            "gender": "female",
            "badge": "YarnGPT AI",
            "is_default": True
        },
        {
            "id": "yarngpt:emma",
            "voice_name": "emma",
            "provider": "yarngpt",
            "display_name": "Prof. Emma",
            "description": "Authoritative, deep resonance — classic senior lecturer cadence.",
            "accent": "Nigerian English",
            "gender": "male",
            "badge": "Senior Scholar",
            "is_default": False
        },
        {
            "id": "yarngpt:umar",
            "voice_name": "umar",
            "provider": "yarngpt",
            "display_name": "Umar",
            "description": "Calm, clear, and structured step-by-step reasoning.",
            "accent": "Nigerian English",
            "gender": "male",
            "badge": "YarnGPT AI",
            "is_default": False
        },
        {
            "id": "yarngpt:chinenye",
            "voice_name": "chinenye",
            "provider": "yarngpt",
            "display_name": "Chinenye",
            "description": "Warm, engaging, and highly relatable campus tutor.",
            "accent": "Nigerian English",
            "gender": "female",
            "badge": "Campus Tutor",
            "is_default": False
        },
        {
            "id": "yarngpt:remi",
            "voice_name": "remi",
            "provider": "yarngpt",
            "display_name": "Remi",
            "description": "Melodious, warm, and encouraging voice.",
            "accent": "Nigerian English",
            "gender": "female",
            "badge": "YarnGPT AI",
            "is_default": False
        },
        {
            "id": "yarngpt:osagie",
            "voice_name": "osagie",
            "provider": "yarngpt",
            "display_name": "Osagie",
            "description": "Smooth, articulate, and steady delivery.",
            "accent": "Nigerian English",
            "gender": "male",
            "badge": "YarnGPT AI",
            "is_default": False
        },
        {
            "id": "yarngpt:nonso",
            "voice_name": "nonso",
            "provider": "yarngpt",
            "display_name": "Nonso",
            "description": "Bold, resonant, confident classroom tone.",
            "accent": "Nigerian English",
            "gender": "male",
            "badge": "YarnGPT AI",
            "is_default": False
        },
        {
            "id": "yarngpt:adaora",
            "voice_name": "adaora",
            "provider": "yarngpt",
            "display_name": "Adaora",
            "description": "Warm, engaging, and friendly pedagogical style.",
            "accent": "Nigerian English",
            "gender": "female",
            "badge": "YarnGPT AI",
            "is_default": False
        }
    ]

    def __init__(self, voice_name: Optional[str] = None):
        self.api_key = settings.YARNGPT_API_KEY
        self.base_url = settings.YARNGPT_BASE_URL.rstrip("/")
        self.voice_name = voice_name or settings.YARNGPT_DEFAULT_VOICE
        self.fallback = EdgeTTSProvider()

    def clean_voice_id(self, voice_id: Optional[str]) -> str:
        """Strips provider prefix like 'yarngpt:' and returns clean lowercase voice name."""
        if not voice_id:
            return self.voice_name
        v = voice_id.strip()
        if v.startswith("yarngpt:"):
            v = v[len("yarngpt:"):]
        return v.lower()

    async def synthesize_scene_audio(
        self,
        script: str,
        output_filepath: str,
        voice_id: Optional[str] = None,
    ) -> float:
        """
        Synthesizes spoken scene text using YarnGPT's streaming prepare endpoint.
        Returns the exact audio duration in seconds.
        Falls back seamlessly to EdgeTTS on any API failure.
        """
        clean_text = EdgeTTSProvider.sanitize_spoken_text(script)
        target_voice = self.clean_voice_id(voice_id)

        # Fallback if no API key is provided
        if not self.api_key:
            logger.warning("[YarnGPT Warning] YARNGPT_API_KEY not configured. Falling back to EdgeTTS.")
            return await self.fallback.synthesize_scene_audio(script, output_filepath)

        os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "text": clean_text,
            "voice": target_voice,
            "output_format": "mp3",
        }

        try:
            async with httpx.AsyncClient(timeout=40.0, follow_redirects=True) as client:
                # 1. Mint streaming ticket
                prepare_resp = await client.post(
                    f"{self.base_url}/api/v1/tts/prepare",
                    json=payload,
                    headers=headers,
                )

                if prepare_resp.status_code != 200:
                    logger.warning(
                        f"[YarnGPT Warning] /tts/prepare returned HTTP {prepare_resp.status_code}: {prepare_resp.text}. Falling back to EdgeTTS."
                    )
                    return await self.fallback.synthesize_scene_audio(script, output_filepath)

                prep_data = prepare_resp.json()
                stream_path = prep_data.get("stream_url")
                if not stream_path:
                    logger.warning("[YarnGPT Warning] No stream_url returned. Falling back to EdgeTTS.")
                    return await self.fallback.synthesize_scene_audio(script, output_filepath)

                stream_url = (
                    f"{self.base_url}{stream_path}"
                    if stream_path.startswith("/")
                    else stream_path
                )

                # 2. Fetch stream (No auth header needed on stream route as ticket in URL is the credential)
                stream_resp = await client.get(stream_url)
                if stream_resp.status_code == 200 and len(stream_resp.content) > 0:
                    with open(output_filepath, "wb") as f:
                        f.write(stream_resp.content)

                    # Validate and determine exact clip duration
                    clip = AudioFileClip(output_filepath)
                    duration = float(clip.duration)
                    clip.close()
                    return duration
                else:
                    logger.warning(
                        f"[YarnGPT Warning] Fetching stream returned {stream_resp.status_code}. Falling back to EdgeTTS."
                    )
                    return await self.fallback.synthesize_scene_audio(script, output_filepath)

        except Exception as e:
            logger.warning(f"[YarnGPT Warning] Exception during synthesis ({e}). Falling back to EdgeTTS.")
            return await self.fallback.synthesize_scene_audio(script, output_filepath)
