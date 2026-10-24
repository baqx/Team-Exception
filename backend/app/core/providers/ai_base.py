from abc import ABC, abstractmethod
from typing import Optional
from app.core.models import LessonPlan

class BaseAIProvider(ABC):
    """
    Abstract Base Class for AI multimodal lesson generation.
    Enables swapping between Gemini, OpenAI, Claude, or Mock providers seamlessly.
    """

    @abstractmethod
    async def generate_lesson_plan(
        self,
        query: str,
        subject: str,
        target_duration_sec: int = 240,
        image_bytes: Optional[bytes] = None,
        image_mime: Optional[str] = None,
        language: Optional[str] = "en",
    ) -> LessonPlan:
        """
        Analyze user query and multimodal image; return strict, validated LessonPlan.
        """
        pass
