import os
import sys
import asyncio
import shutil
import subprocess
import imageio_ffmpeg

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir = os.path.dirname(backend_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.services.factory import get_ai_provider, get_tts_provider
from app.services.video.chalkboard_renderer import ChalkboardRenderer
from app.services.video.stitcher import VideoStitcher
from app.core.models import LessonPlan

async def generate_and_stitch():
    print("=== Generating Full 4-Scene Chalkka Lesson ===")
    ai = get_ai_provider()
    lesson: LessonPlan = await ai.generate_lesson_plan(
        query="Solve integral of x * ln(x) dx using integration by parts",
        subject="Calculus",
        target_duration_sec=90,
    )

    tts = get_tts_provider()
    renderer = ChalkboardRenderer(width=1280, height=720, fps=24)

    output_dir = os.path.join(backend_dir, "full_lesson_output")
    os.makedirs(output_dir, exist_ok=True)

    scene_clips = []
    persistent_items = []
    start_y = 50
    for idx, scene in enumerate(lesson.scenes):
        print(f"\n--- Scene {scene.step_number}: {scene.title} ---")
        audio_file = os.path.join(output_dir, f"scene_{idx + 1}_audio.mp3")
        video_file = os.path.join(output_dir, f"scene_{idx + 1}_clip.mp4")

        # Synthesize audio with calm teacher pacing
        duration = await tts.synthesize_scene_audio(scene.spoken_script, audio_file)
        print(f"  Audio synthesized ({duration:.2f}s)")

        # Render clip with cumulative blackboard writing
        _, persistent_items, start_y = renderer.render_scene_clip(
            scene=scene,
            audio_path=audio_file,
            output_path=video_file,
            persistent_items=persistent_items,
            start_y=start_y,
        )
        print(f"  Clip rendered: {video_file} ({os.path.getsize(video_file)} bytes), next Y: {start_y}")
        scene_clips.append(video_file)

    # Stitch all scenes together
    stitched_file = os.path.join(output_dir, "final_stitched_lesson.mp4")
    print(f"\nStitching {len(scene_clips)} scenes...")
    VideoStitcher.stitch_scenes(scene_clips, stitched_file)
    print(f"Stitched lesson: {stitched_file} ({os.path.getsize(stitched_file)} bytes)")

    # Copy to Next.js public directory
    public_file = os.path.join(root_dir, "public", "demo_lesson.mp4")
    shutil.copyfile(stitched_file, public_file)
    print(f"Copied to Next.js public: {public_file} ({os.path.getsize(public_file)} bytes)")

    # Validate with FFmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    check = subprocess.run([ffmpeg, "-v", "error", "-i", public_file, "-f", "null", "-"], stderr=subprocess.PIPE, text=True)
    if check.stderr.strip() == "":
        print("FFmpeg integrity check: 0 errors! Video stream is perfectly healthy.")
    else:
        print(f"FFmpeg notice: {check.stderr}")

    print("\n=== Lesson Generation Complete! ===")

if __name__ == "__main__":
    asyncio.run(generate_and_stitch())
