import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.api.router import api_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for Chalkka — The AI Chalkboard Explainer Video Tutor",
    version="1.0.0",
)

# CORS Middleware
allowed_origins = list(settings.CORS_ORIGINS)
env_frontend = os.environ.get("FRONTEND_URL")
if env_frontend and env_frontend not in allowed_origins:
    allowed_origins.append(env_frontend)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount local video storage as static files
os.makedirs(settings.LOCAL_STORAGE_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=settings.LOCAL_STORAGE_DIR), name="static")

# Mount API routes
app.include_router(api_router, prefix="/api")

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "providers": {
            "ai": settings.AI_PROVIDER,
            "tts": settings.TTS_PROVIDER,
            "storage": settings.STORAGE_PROVIDER,
        }
    }

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Chalkka Video Generation API is active.",
        "docs": "/docs",
        "health": "/health",
    }
