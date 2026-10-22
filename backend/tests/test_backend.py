import os
import sys
import asyncio

# Add backend directory to sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.services.factory import get_ai_provider, get_tts_provider, get_storage_provider
from app.services.video.chalkboard_renderer import ChalkboardRenderer
from app.services.video.stitcher import VideoStitcher
from app.core.models import LessonPlan

async def test_end_to_end_pipeline():
    print("=== Testing Chalkka Backend Pipeline ===")
    
    # 1. AI Provider Test
    print("[1/4] Testing AI Provider (Mock / Gemini)...")
    ai = get_ai_provider()
    lesson: LessonPlan = await ai.generate_lesson_plan(
        query="Solve integral of x * ln(x) dx using integration by parts",
        subject="Calculus",
        target_duration_sec=120,
    )
    assert lesson.problem_title != ""
    assert len(lesson.scenes) >= 3
    print(f"  [OK] Lesson Plan Generated: '{lesson.problem_title}' with {len(lesson.scenes)} scenes.")

    # 2. TTS Voice Synthesis Test
    print("[2/4] Testing TTS Provider (Edge-TTS)...")
    tts = get_tts_provider()
    test_dir = os.path.join(backend_dir, "test_output")
    os.makedirs(test_dir, exist_ok=True)
    
    test_audio = os.path.join(test_dir, "test_scene_1.mp3")
    duration = await tts.synthesize_scene_audio(
        script="So let's work through this problem together. We want to evaluate the indefinite integral of x times the natural log of x.",
        output_filepath=test_audio,
    )
    assert duration > 1.0
    print(f"  [OK] Voice Audio Synthesized: {duration:.2f}s duration saved to {test_audio}")

    # 3. Video Rendering Test
    print("[3/4] Testing Chalkboard Video Rendering...")
    renderer = ChalkboardRenderer(width=1280, height=720, fps=15)
    test_video = os.path.join(test_dir, "test_clip_1.mp4")
    renderer.render_scene_clip(
        scene=lesson.scenes[0],
        audio_path=test_audio,
        output_path=test_video,
    )
    assert os.path.exists(test_video)
    print(f"  [OK] Chalkboard Video Rendered: {test_video} ({os.path.getsize(test_video)} bytes)")

    # 4. Storage Provider Test
    print("[4/4] Testing Storage Provider (Local / Cloudinary)...")
    storage = get_storage_provider()
    url = await storage.upload_video(
        local_filepath=test_video,
        destination_filename="demo_lesson_test.mp4",
    )
    assert url.startswith("http") or url.startswith("/static")
    print(f"  [OK] Storage Provider Verified: Video served at {url}")

    # 5. Stitcher Verification Test
    print("[5/5] Testing Faststart Video Stitcher...")
    stitched_output = os.path.join(test_dir, "test_stitched_lesson.mp4")
    VideoStitcher.stitch_scenes([test_video, test_video], stitched_output)
    assert os.path.exists(stitched_output)
    assert os.path.getsize(stitched_output) > 1000
    print(f"  [OK] Faststart Video Stitched: {stitched_output} ({os.path.getsize(stitched_output)} bytes)")

    print("\n=== ALL PIPELINE TESTS PASSED! ===")

if __name__ == "__main__":
    asyncio.run(test_end_to_end_pipeline())
