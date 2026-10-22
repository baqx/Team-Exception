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

async def generate_nitrogen_cycle_full_lesson():
    print("=" * 65)
    print(" Generating Full Nitrogen Cycle Chalkboard Lesson Video ")
    print("=" * 65)

    # 1. Generate Lesson Plan
    ai = get_ai_provider()
    lesson: LessonPlan = await ai.generate_lesson_plan(
        query="Explain how the nitrogen cycle works from atmospheric N2 triple bond to soil bacteria fixation, nitrification, and back to the air",
        subject="Biology",
        target_duration_sec=160,
    )

    print(f"\n[1/4] Lesson Plan Loaded: '{lesson.problem_title}'")
    print(f"  Subject: {lesson.subject}")
    print(f"  Concept: {lesson.core_concept}")
    print(f"  Total Scenes: {len(lesson.scenes)}")

    tts = get_tts_provider()
    renderer = ChalkboardRenderer(width=1280, height=720, fps=24)

    output_dir = os.path.join(backend_dir, "full_nitrogen_output")
    os.makedirs(output_dir, exist_ok=True)

    scene_clips = []
    persistent_items = []
    start_y = 50

    # 2. Render each scene clip
    print("\n[2/4] Synthesizing Audio & Rendering Chalkboard Clips...")
    for idx, scene in enumerate(lesson.scenes):
        print(f"\n--- Scene {scene.step_number}/{len(lesson.scenes)}: {scene.title} [{scene.category}] ---")
        audio_file = os.path.join(output_dir, f"scene_{idx + 1}_audio.mp3")
        video_file = os.path.join(output_dir, f"scene_{idx + 1}_clip.mp4")

        # Synthesize audio with natural teacher delivery & math sanitizer
        duration = await tts.synthesize_scene_audio(scene.spoken_script, audio_file)
        print(f"  Voice narration synthesized: {duration:.2f}s -> {audio_file}")

        # Render chalkboard video clip
        _, persistent_items, start_y = renderer.render_scene_clip(
            scene=scene,
            audio_path=audio_file,
            output_path=video_file,
            persistent_items=persistent_items,
            start_y=start_y,
        )
        print(f"  Chalkboard clip rendered: {video_file} ({os.path.getsize(video_file):,} bytes)")
        scene_clips.append(video_file)

    # 3. Stitch all scenes into full lesson
    print("\n[3/4] Faststart Concatenation & Normalization...")
    stitched_file = os.path.join(output_dir, "nitrogen_cycle_full_lesson.mp4")
    VideoStitcher.stitch_scenes(scene_clips, stitched_file)
    print(f"  Stitched video ready: {stitched_file} ({os.path.getsize(stitched_file):,} bytes)")

    # 4. Copy to public directory for immediate web playback
    public_dest = os.path.join(root_dir, "public", "nitrogen_cycle_lesson.mp4")
    shutil.copyfile(stitched_file, public_dest)
    print(f"\n[4/4] Copied to public web directory: {public_dest} ({os.path.getsize(public_dest):,} bytes)")

    # Also update demo_lesson.mp4 so the hero/demo player shows the Nitrogen Cycle video
    demo_dest = os.path.join(root_dir, "public", "demo_lesson.mp4")
    shutil.copyfile(stitched_file, demo_dest)
    print(f"  Updated demo_lesson.mp4 with Nitrogen Cycle video!")

    # Faststart & MP4 integrity validation
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    check = subprocess.run([ffmpeg, "-v", "error", "-i", public_dest, "-f", "null", "-"], stderr=subprocess.PIPE, text=True)
    if not check.stderr.strip():
        print("  FFmpeg stream integrity verified: 0 errors! Adaptive streaming ready.")
    else:
        print(f"  FFmpeg notice: {check.stderr}")

    print("\n" + "=" * 65)
    print(" Full Nitrogen Cycle Video Generation Completed Successfully! ")
    print("=" * 65)

if __name__ == "__main__":
    asyncio.run(generate_nitrogen_cycle_full_lesson())
