import os
import sys
import asyncio
from PIL import Image

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.services.factory import get_ai_provider, get_tts_provider
from app.services.video.chalkboard_renderer import ChalkboardRenderer
from app.core.models import LessonPlan
from moviepy import VideoFileClip

async def main():
    print("Testing Scene 3 render & cancelation kinematics...")
    ai = get_ai_provider()
    lesson: LessonPlan = await ai.generate_lesson_plan(
        query="Solve integral of x * ln(x) dx using integration by parts",
        subject="Calculus",
    )
    # Scene 3: Substitution into By-Parts Formula
    scene3 = lesson.scenes[2]
    print(f"Scene 3 title: {scene3.title}")
    print(f"Actions in Scene 3: {len(scene3.chalk_actions)}")
    for a in scene3.chalk_actions:
        print(f" - {a.action_type}: {a.content}")

    tts = get_tts_provider()
    out_dir = os.path.join(backend_dir, "test_output")
    os.makedirs(out_dir, exist_ok=True)
    audio_path = os.path.join(out_dir, "scene_3_audio.mp3")

    duration = await tts.synthesize_scene_audio(scene3.spoken_script, audio_path)
    print(f"Synthesized scene 3 audio: {duration:.2f}s")

    renderer = ChalkboardRenderer(width=1280, height=720, fps=24)
    clip_path = os.path.join(out_dir, "scene_3_clip.mp4")
    renderer.render_scene_clip(scene3, audio_path, clip_path)
    print(f"Rendered scene 3 clip: {clip_path} ({os.path.getsize(clip_path)} bytes)")

    # Extract test frames to verify visually
    clip = VideoFileClip(clip_path)
    timestamps = [duration * 0.25, duration * 0.55, duration * 0.85]
    for idx, ts in enumerate(timestamps):
        frame = clip.get_frame(ts)
        frame_img = Image.fromarray(frame)
        frame_path = os.path.join(out_dir, f"scene_3_frame_{idx}.png")
        frame_img.save(frame_path)
        print(f"Saved snapshot at t={ts:.2f}s: {frame_path}")
    clip.close()
    print("Scene 3 verification completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())
