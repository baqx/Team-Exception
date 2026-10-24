from fastapi import APIRouter
from app.api.endpoints.generate import router as generate_router
from app.api.endpoints.regenerate import router as regenerate_router
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.voices import router as voices_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="", tags=["Auth & User"])
api_router.include_router(generate_router, prefix="", tags=["Generation"])
api_router.include_router(regenerate_router, prefix="", tags=["Regeneration"])
api_router.include_router(voices_router, prefix="", tags=["Voices"])

