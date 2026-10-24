import os
from typing import List
from pydantic_settings import BaseSettings

# Resolve potential locations for .env files across backend and workspace root
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # backend directory
_ROOT_DIR = os.path.dirname(_BASE_DIR)                                  # project root directory

_ENV_FILES = [
    f for f in [
        os.path.join(_BASE_DIR, ".env"),
        os.path.join(_ROOT_DIR, ".env.local"),
        os.path.join(_ROOT_DIR, ".env"),
        os.path.join(_ROOT_DIR, ".env.lc"),
        ".env",
    ] if os.path.exists(f)
]

class Settings(BaseSettings):
    APP_NAME: str = "Chalkka Backend API"
    APP_ENV: str = "production"
    DEBUG: bool = True
    PORT: int = 8000

    # Provider Toggles (Easily swappable via .env)
    AI_PROVIDER: str = "gemini"        # Options: "gemini", "mock"
    TTS_PROVIDER: str = "edge"          # Options: "edge", "google", "mock"
    STORAGE_PROVIDER: str = "cloudinary"  # Options: "local", "cloudinary", "supabase"

    # AI Configuration (Gemini)
    GOOGLE_GENERATIVE_AI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3-flash-preview"

    # Audio / TTS Configuration
    EDGE_TTS_VOICE: str = "en-US-ChristopherNeural"  # Calm, authoritative academic voice
    YARNGPT_API_KEY: str = ""
    YARNGPT_BASE_URL: str = "https://api.yarngpt.ai"
    YARNGPT_DEFAULT_VOICE: str = "idera"
    GOOGLE_APPLICATION_CREDENTIALS: str = ""

    # Storage: Cloudinary
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    # Supabase (Storage, Database & Auth)
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_PUBLISHABLE_KEY: str = ""
    SUPABASE_SECRET_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    SUPABASE_JWKS_URL: str = ""

    # Storage: Local directory path
    LOCAL_STORAGE_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static_storage")

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]

    class Config:
        env_file = _ENV_FILES
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

# Ensure local storage directory exists
os.makedirs(settings.LOCAL_STORAGE_DIR, exist_ok=True)
