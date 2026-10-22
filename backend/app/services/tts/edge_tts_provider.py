import asyncio
import os
import re
import struct
import wave
import shutil
from typing import Optional
import edge_tts
from moviepy import AudioFileClip
from app.config import settings
from app.core.providers.tts_base import BaseTTSProvider

class EdgeTTSProvider(BaseTTSProvider):
    """
    High-fidelity natural voice provider powered by Microsoft Edge TTS.
    Completely free, requires no API keys or cloud billing, and supports SSML pacing.
    Includes automated retry logic and offline fallback audio to ensure rendering pipelines never fail.
    """

    def __init__(self, voice_name: Optional[str] = None):
        self.voice_name = voice_name or settings.EDGE_TTS_VOICE

    @classmethod
    def sanitize_spoken_text(cls, text: str) -> str:
        """
        Translates raw LaTeX notation, chemical formulas, and technical markup
        into natural spoken English words for Edge-TTS.
        """
        s = text

        # Handle fractions: \frac{a}{b} -> a over b
        s = re.sub(r"\\frac\{([^}]+)\}\{([^}]+)\}", r"\1 over \2", s)
        
        # Handle integrals and roots
        s = re.sub(r"\\int_\{([^}]+)\}\^\{([^}]+)\}", r"the integral from \1 to \2 of", s)
        s = s.replace(r"\int", "the integral of ")
        s = re.sub(r"\\sqrt\{([^}]+)\}", r"the square root of \1", s)
        s = re.sub(r"\\ln\(([^)]+)\)", r"natural log of \1", s)
        s = s.replace(r"\ln", "natural log ")

        # Handle chemical / arrow notation
        s = s.replace(r"\rightarrow", " yields ")
        s = s.replace(r"\implies", " which gives ")
        s = s.replace("-->", " yields ")
        s = s.replace("->", " yields ")

        # Common math symbols
        s = s.replace(r"\cdot", " times ")
        s = s.replace(r"\times", " times ")
        s = s.replace(r"\approx", " approximately ")
        s = s.replace(r"\pm", " plus or minus ")
        s = s.replace(r"\parallel", " in parallel with ")
        s = s.replace(r"\Omega", " ohms ")
        s = s.replace(r"\,", " ")
        s = s.replace(r"\;", " ")

        # Strip boxed or text wrappers
        s = re.sub(r"\\boxed\{([^}]+)\}", r"\1", s)
        s = re.sub(r"\\text\{([^}]+)\}", r"\1", s)

        # Convert SSML break tags and multiple dots into natural teacher breath pauses
        s = re.sub(r"<break[^>]*>", " ... ", s)
        s = re.sub(r"<[^>]+>", "", s)
        s = re.sub(r"\.{3,}", " ... ", s)

        # Strip remaining backslashes and LaTeX delimiters
        s = re.sub(r"\\[a-zA-Z]+", " ", s)
        s = s.replace("{", " ").replace("}", " ").replace("$", "")
        s = re.sub(r"\s+", " ", s).strip()
        return s

    def _generate_fallback_audio(self, text: str, output_filepath: str) -> float:
        """
        Generates clean offline PCM audio clip when Microsoft Edge TTS cannot be reached
        (e.g., DNS error 'getaddrinfo failed', temporary network drop, or offline work),
        allowing the chalkboard video rendering pipeline to continue without crashing.
        """
        words = len(text.split())
        # Estimate natural instructional duration: ~2.3 words/sec, minimum 3.0 seconds
        estimated_duration = max(3.0, round(words / 2.3, 2))
        sample_rate = 24000
        num_samples = int(estimated_duration * sample_rate)

        fallback_wav = output_filepath if output_filepath.endswith(".wav") else output_filepath + ".wav"
        with wave.open(fallback_wav, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            # Empty PCM silence
            data = struct.pack("<" + ("h" * num_samples), *([0] * num_samples))
            wf.writeframes(data)

        if fallback_wav != output_filepath:
            shutil.copyfile(fallback_wav, output_filepath)
            try:
                os.remove(fallback_wav)
            except OSError:
                pass

        return float(estimated_duration)

    async def synthesize_scene_audio(
        self,
        script: str,
        output_filepath: str,
        voice_id: Optional[str] = None,
    ) -> float:
        voice = voice_id or self.voice_name
        clean_text = self.sanitize_spoken_text(script)

        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)

        # Retry up to 3 times to withstand transient DNS resolution / socket errors
        max_retries = 3
        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                communicate = edge_tts.Communicate(clean_text, voice, rate="-5%")
                await communicate.save(output_filepath)

                # Validate saved audio file
                if os.path.exists(output_filepath) and os.path.getsize(output_filepath) > 0:
                    audio_clip = AudioFileClip(output_filepath)
                    duration = float(audio_clip.duration)
                    audio_clip.close()
                    return duration
            except Exception as err:
                last_error = err
                print(f"[EdgeTTS Warning] Attempt {attempt}/{max_retries} failed ({err}).")
                if attempt < max_retries:
                    await asyncio.sleep(1.0 * attempt)

        # If network/DNS to speech.platform.bing.com failed across all retries, fall back gracefully
        print(f"[EdgeTTS Warning] All {max_retries} TTS attempts failed ({last_error}). Using offline audio fallback.")
        return self._generate_fallback_audio(clean_text, output_filepath)
