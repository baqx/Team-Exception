import os
import uuid
import asyncio
from typing import Dict, Optional
from app.core.models import JobStatus, LessonPlan
from app.services.factory import get_ai_provider, get_tts_provider, get_storage_provider
from app.services.video.chalkboard_renderer import ChalkboardRenderer
from app.services.video.stitcher import VideoStitcher

# In-memory job repository
jobs: Dict[str, JobStatus] = {}

class VideoGenerationWorker:
    def __init__(self, work_dir: str = "temp_render_workspace"):
        self.work_dir = os.path.abspath(work_dir)
        os.makedirs(self.work_dir, exist_ok=True)
        self.renderer = ChalkboardRenderer()

    async def run_generation_job(
        self,
        job_id: str,
        query: str,
        subject: str,
        target_duration_sec: int,
        image_bytes: Optional[bytes] = None,
        image_mime: Optional[str] = None,
        user_id: Optional[str] = None,
    ):
        from app.services import user_service
        job_dir = os.path.join(self.work_dir, job_id)
        os.makedirs(job_dir, exist_ok=True)

        try:
            # 1. Analyzing & Lesson Planning
            jobs[job_id].status = "analyzing"
            jobs[job_id].progress_percent = 15
            jobs[job_id].current_step_text = "Diagnosing prerequisites & structuring lesson..."

            ai = get_ai_provider()
            lesson_plan: LessonPlan = await ai.generate_lesson_plan(
                query=query,
                subject=subject,
                target_duration_sec=target_duration_sec,
                image_bytes=image_bytes,
                image_mime=image_mime,
            )
            jobs[job_id].lesson_plan = lesson_plan

            # 2. Audio Voice Synthesis
            jobs[job_id].status = "synthesizing_audio"
            jobs[job_id].progress_percent = 40
            jobs[job_id].current_step_text = "Synthesizing voice narration with classroom pacing..."

            tts = get_tts_provider()
            scene_audio_paths = []
            for scene in lesson_plan.scenes:
                audio_path = os.path.join(job_dir, f"audio_scene_{scene.step_number}.mp3")
                await tts.synthesize_scene_audio(
                    script=scene.spoken_script,
                    output_filepath=audio_path,
                )
                scene_audio_paths.append(audio_path)

            # 3. Video Rendering
            jobs[job_id].status = "rendering_video"
            jobs[job_id].progress_percent = 70
            jobs[job_id].current_step_text = "Drawing chalkboard equations & circuit schematics..."

            scene_video_paths = []
            persistent_items = []
            start_y = 50
            for scene, audio_path in zip(lesson_plan.scenes, scene_audio_paths):
                video_path = os.path.join(job_dir, f"clip_scene_{scene.step_number}.mp4")
                loop = asyncio.get_event_loop()
                _, persistent_items, start_y = await loop.run_in_executor(
                    None,
                    self.renderer.render_scene_clip,
                    scene,
                    audio_path,
                    video_path,
                    persistent_items,
                    start_y,
                )
                scene_video_paths.append(video_path)

            # 4. Audio/Video Stitching
            jobs[job_id].status = "stitching"
            jobs[job_id].progress_percent = 85
            jobs[job_id].current_step_text = "Assembling full chalkboard video & normalizing audio..."

            final_stitched_path = os.path.join(job_dir, "final_lesson.mp4")
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                VideoStitcher.stitch_scenes,
                scene_video_paths,
                final_stitched_path,
            )

            # 5. Storage Upload
            jobs[job_id].progress_percent = 95
            jobs[job_id].current_step_text = "Uploading video to CDN for adaptive streaming..."

            storage = get_storage_provider()
            video_url = await storage.upload_video(
                local_filepath=final_stitched_path,
                destination_filename=f"lesson_{job_id}.mp4",
            )

            # Completed
            jobs[job_id].status = "completed"
            jobs[job_id].progress_percent = 100
            jobs[job_id].current_step_text = "Tutor video generated and ready!"
            jobs[job_id].video_url = video_url

            # Record completion in persistent user store
            user_service.record_job_completion(
                job_id=job_id,
                video_url=video_url,
                lesson_plan_dict=lesson_plan.model_dump() if lesson_plan else None
            )

        except Exception as e:
            jobs[job_id].status = "failed"
            jobs[job_id].error_message = str(e)
            jobs[job_id].current_step_text = f"Failed: {str(e)}"
            user_service.record_job_failure(job_id=job_id, error_message=str(e))

    async def run_step_regeneration_job(
        self,
        job_id: str,
        step_number: int,
        focus_angle: str = "",
    ):
        job_dir = os.path.join(self.work_dir, job_id)
        if job_id not in jobs or not jobs[job_id].lesson_plan:
            return

        try:
            jobs[job_id].status = "analyzing"
            jobs[job_id].current_step_text = f"Re-deriving Step {step_number} with alternate intuition..."
            jobs[job_id].progress_percent = 30

            lesson_plan = jobs[job_id].lesson_plan
            target_idx = max(0, min(len(lesson_plan.scenes) - 1, step_number - 1))
            scene = lesson_plan.scenes[target_idx]

            # Re-synthesize audio for this step with natural pacing
            jobs[job_id].status = "synthesizing_audio"
            jobs[job_id].current_step_text = f"Re-synthesizing voice explanation for Step {step_number}..."
            jobs[job_id].progress_percent = 50

            tts = get_tts_provider()
            audio_path = os.path.join(job_dir, f"audio_scene_{scene.step_number}.mp3")
            await tts.synthesize_scene_audio(
                script=scene.spoken_script,
                output_filepath=audio_path,
            )

            # Re-render scene clips
            jobs[job_id].status = "rendering_video"
            jobs[job_id].current_step_text = f"Re-drawing chalkboard derivation for Step {step_number}..."
            jobs[job_id].progress_percent = 75

            scene_video_paths = []
            persistent_items = []
            start_y = 50
            for s in lesson_plan.scenes:
                s_audio_path = os.path.join(job_dir, f"audio_scene_{s.step_number}.mp3")
                s_video_path = os.path.join(job_dir, f"clip_scene_{s.step_number}.mp4")
                loop = asyncio.get_event_loop()
                _, persistent_items, start_y = await loop.run_in_executor(
                    None,
                    self.renderer.render_scene_clip,
                    s,
                    s_audio_path,
                    s_video_path,
                    persistent_items,
                    start_y,
                )
                scene_video_paths.append(s_video_path)

            # Re-stitch
            jobs[job_id].status = "stitching"
            jobs[job_id].current_step_text = "Re-assembling updated lesson video..."
            jobs[job_id].progress_percent = 90

            final_stitched_path = os.path.join(job_dir, "final_lesson.mp4")
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                VideoStitcher.stitch_scenes,
                scene_video_paths,
                final_stitched_path,
            )

            # Upload to storage
            storage = get_storage_provider()
            video_url = await storage.upload_video(
                local_filepath=final_stitched_path,
                destination_filename=f"lesson_{job_id}.mp4",
            )

            jobs[job_id].status = "completed"
            jobs[job_id].progress_percent = 100
            jobs[job_id].current_step_text = f"Step {step_number} successfully regenerated and ready!"
            jobs[job_id].video_url = video_url

        except Exception as e:
            jobs[job_id].status = "failed"
            jobs[job_id].error_message = str(e)
            jobs[job_id].current_step_text = f"Regeneration failed: {str(e)}"

worker = VideoGenerationWorker()
