from fastapi import APIRouter
from typing import List, Dict, Any
from app.services.tts.yarngpt_provider import YarnGPTProvider

router = APIRouter()

STANDARD_EDGE_VOICES: List[Dict[str, Any]] = [
    {
        "id": "edge:en-US-ChristopherNeural",
        "voice_name": "Christopher",
        "provider": "edge",
        "display_name": "Dr. Christopher",
        "description": "Calm, authoritative professor with deliberate lecture pacing.",
        "accent": "Global Academic (US)",
        "gender": "male",
        "badge": "Standard",
        "is_default": True
    },
    {
        "id": "edge:en-US-JennyNeural",
        "voice_name": "Jenny",
        "provider": "edge",
        "display_name": "Prof. Jenny",
        "description": "Clear, friendly, and structured academic delivery.",
        "accent": "Global Academic (US)",
        "gender": "female",
        "badge": "Standard",
        "is_default": False
    }
]

@router.get("/voices", response_model=List[Dict[str, Any]])
async def list_available_tutor_voices():
    """
    Returns available tutor voices across Edge-TTS (Global Academic) 
    and YarnGPT (African Voice AI).
    """
    return STANDARD_EDGE_VOICES + YarnGPTProvider.CATALOG
