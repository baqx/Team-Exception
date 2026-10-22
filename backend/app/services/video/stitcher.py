import os
import subprocess
from typing import List
import imageio_ffmpeg
from moviepy import VideoFileClip, concatenate_videoclips

class VideoStitcher:
    """
    Stitches individual scene clips into a single finalized MP4 lesson.
    Uses ultrafast ffmpeg concat stream copy with faststart headers, ensuring
    instant web streaming and zero file corruption.
    """

    @staticmethod
    def stitch_scenes(scene_clip_paths: List[str], output_path: str) -> str:
        if not scene_clip_paths:
            raise ValueError("No scene clips provided to stitch.")

        output_dir = os.path.dirname(os.path.abspath(output_path))
        os.makedirs(output_dir, exist_ok=True)

        # 1. Direct ffmpeg stream copy with +faststart (runs in ~0.2s without re-encoding)
        try:
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            list_txt_path = os.path.join(output_dir, "concat_clips.txt")
            with open(list_txt_path, "w", encoding="utf-8") as f:
                for p in scene_clip_paths:
                    clean_p = os.path.abspath(p).replace("\\", "/")
                    f.write(f"file '{clean_p}'\n")

            cmd = [
                ffmpeg_exe,
                "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", list_txt_path,
                "-c", "copy",
                "-movflags", "+faststart",
                output_path,
            ]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
                return output_path
        except Exception:
            pass

        # Clean up any partial output before fallback
        if os.path.exists(output_path) and os.path.getsize(output_path) < 1000:
            try:
                os.remove(output_path)
            except Exception:
                pass

        # 2. MoviePy fallback with +faststart
        clips = [VideoFileClip(p) for p in scene_clip_paths]
        final_video = concatenate_videoclips(clips, method="compose")
        final_video.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            ffmpeg_params=["-movflags", "+faststart"],
            logger=None
        )
        for c in clips:
            c.close()
        final_video.close()

        return output_path
