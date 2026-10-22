import os
import sys
import asyncio
from PIL import Image

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.services.factory import get_ai_provider, get_tts_provider
from app.services.video.chalkboard_renderer import ChalkboardRenderer
from app.services.video.schematic_renderer import SchematicRenderer
from app.services.tts.edge_tts_provider import EdgeTTSProvider
from app.core.models import LessonPlan

async def test_nitrogen_cycle_pipeline():
    print("=== Testing Nitrogen Cycle & Schematic Video Engine ===")

    # 1. Spoken Math Sanitizer Test
    print("[1/5] Testing Spoken Math Sanitizer...")
    raw_math = r"First, we calculate \frac{x^2}{2} and then \int u \, dv \implies 2\text{NH}_4^+ + 3\text{O}_2 \rightarrow 2\text{NO}_2^-"
    sanitized = EdgeTTSProvider.sanitize_spoken_text(raw_math)
    print(f"  Raw:       {raw_math}")
    print(f"  Sanitized: {sanitized}")
    assert "backslash" not in sanitized.lower()
    assert r"\frac" not in sanitized
    assert "yields" in sanitized
    print("  [OK] Math Sanitizer successfully purged raw LaTeX for natural speech.")

    # 2. Schematic Renderer Direct Test (Nitrogen Cycle & Circuit)
    print("\n[2/5] Testing Schematic Renderer...")
    diag_img, trace_pts = SchematicRenderer.render_nitrogen_cycle_diagram(width=1000, height=360)
    assert diag_img.size == (1000, 360)
    assert len(trace_pts) > 10
    out_dir = os.path.join(backend_dir, "test_output")
    os.makedirs(out_dir, exist_ok=True)
    diag_path = os.path.join(out_dir, "test_nitrogen_diagram.png")
    diag_img.save(diag_path)
    print(f"  [OK] Nitrogen Cycle Schematic rendered and saved to {diag_path}")

    circuit_img, _ = SchematicRenderer.render_circuit_schematic(width=860, height=300)
    circuit_path = os.path.join(out_dir, "test_circuit_diagram.png")
    circuit_img.save(circuit_path)
    print(f"  [OK] Circuit Schematic rendered and saved to {circuit_path}")

    # 3. AI Provider Generation for Nitrogen Cycle Query
    print("\n[3/5] Testing AI Provider for 'Explain the Nitrogen Cycle'...")
    ai = get_ai_provider()
    lesson: LessonPlan = await ai.generate_lesson_plan(
        query="Explain how the nitrogen cycle works from atmospheric N2 to plants and back to the air",
        subject="Biology",
        target_duration_sec=120,
    )
    assert "nitrogen" in lesson.problem_title.lower() or "nitrogen" in lesson.core_concept.lower()
    print(f"  [OK] Lesson Plan generated: '{lesson.problem_title}'")
    print(f"  Number of scenes: {len(lesson.scenes)}")
    for s in lesson.scenes:
        print(f"   * Scene {s.step_number} [{s.category}]: {s.title} ({len(s.chalk_actions)} actions)")
        for a in s.chalk_actions:
            print(f"       - {a.action_type} (timing={a.timing}, color={a.color}): {a.content[:50]}...")

    # 4. Audio Synthesis for Scene 2 (The Schematic Scene)
    print("\n[4/5] Testing Voice Synthesis for Nitrogen Cycle Scene 2...")
    tts = get_tts_provider()
    scene2 = lesson.scenes[1]
    audio_path = os.path.join(out_dir, "nitrogen_scene_2_audio.mp3")
    duration = await tts.synthesize_scene_audio(scene2.spoken_script, audio_path)
    assert duration > 1.0
    print(f"  [OK] Audio synthesized: {duration:.2f}s saved to {audio_path}")

    # 5. Video Rendering for Nitrogen Cycle Scene with Schematic
    print("\n[5/5] Testing Chalkboard Video Rendering of Nitrogen Cycle Scene 2...")
    renderer = ChalkboardRenderer(width=1280, height=720, fps=24)
    clip_path = os.path.join(out_dir, "nitrogen_scene_2_clip.mp4")
    out_path, completed_items, next_y = renderer.render_scene_clip(
        scene=scene2,
        audio_path=audio_path,
        output_path=clip_path,
    )
    assert os.path.exists(clip_path)
    assert os.path.getsize(clip_path) > 10000
    print(f"  [OK] Nitrogen Cycle Video Clip rendered successfully!")
    print(f"  Output: {clip_path} ({os.path.getsize(clip_path)} bytes)")

    print("\n=== ALL NITROGEN CYCLE & SCHEMATIC TESTS PASSED! ===")

if __name__ == "__main__":
    asyncio.run(test_nitrogen_cycle_pipeline())
