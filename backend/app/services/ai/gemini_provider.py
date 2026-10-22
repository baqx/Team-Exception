import json
from typing import Optional
import google.generativeai as genai
from app.config import settings
from app.core.models import LessonPlan
from app.core.providers.ai_base import BaseAIProvider
from app.core.prompts import ORGANIC_CHEMISTRY_TUTOR_SYSTEM_PROMPT, USER_LESSON_PLAN_PROMPT_TEMPLATE

class GeminiProvider(BaseAIProvider):
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or settings.GOOGLE_GENERATIVE_AI_API_KEY
        self.model_name = model_name or settings.GEMINI_MODEL
        if self.api_key:
            genai.configure(api_key=self.api_key, transport="rest")

    async def generate_lesson_plan(
        self,
        query: str,
        subject: str,
        target_duration_sec: int = 240,
        image_bytes: Optional[bytes] = None,
        image_mime: Optional[str] = None,
    ) -> LessonPlan:
        if not self.api_key:
            raise ValueError("GOOGLE_GENERATIVE_AI_API_KEY is not set. Please provide a key or switch AI_PROVIDER='mock'.")

        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=ORGANIC_CHEMISTRY_TUTOR_SYSTEM_PROMPT,
            generation_config={"response_mime_type": "application/json"}
        )

        effective_subject = subject if subject and subject != "general" else "auto"
        num_scenes = max(3, min(8, target_duration_sec // 60))
        prompt_text = USER_LESSON_PLAN_PROMPT_TEMPLATE.format(
            subject=effective_subject,
            target_duration_sec=target_duration_sec,
            num_scenes=num_scenes,
            query=query,
        )

        content_parts = [prompt_text]
        if image_bytes and image_mime:
            content_parts.append({
                "mime_type": image_mime,
                "data": image_bytes,
            })

        try:
            response = model.generate_content(content_parts)
            raw_text = response.text.strip()
            
            # Robust JSON extraction: slice strictly between first '{' and last '}'
            start_idx = raw_text.find("{")
            end_idx = raw_text.rfind("}")
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_str = raw_text[start_idx:end_idx + 1]
            else:
                json_str = raw_text

            parsed_data = json.loads(json_str.strip())
            return LessonPlan.model_validate(parsed_data)
        except Exception as e:
            print(f"[GeminiProvider Warning] Live generation failed: {e}. Falling back to smart offline provider.")
            from app.services.ai.mock_provider import MockAIProvider
            return await MockAIProvider().generate_lesson_plan(
                query=query,
                subject=subject,
                target_duration_sec=target_duration_sec,
                image_bytes=image_bytes,
                image_mime=image_mime,
            )
