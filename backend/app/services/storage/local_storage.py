import os
import shutil
from app.config import settings
from app.core.providers.storage_base import BaseStorageProvider

class LocalStorageProvider(BaseStorageProvider):
    """
    Local filesystem storage provider.
    Saves videos to static directory and syncs to frontend public folder for immediate playback.
    """

    def __init__(self, base_dir: str = settings.LOCAL_STORAGE_DIR, port: int = settings.PORT):
        self.base_dir = base_dir
        self.port = port
        os.makedirs(self.base_dir, exist_ok=True)

    async def upload_video(
        self,
        local_filepath: str,
        destination_filename: str,
    ) -> str:
        destination_path = os.path.join(self.base_dir, destination_filename)
        
        # Copy to backend static storage directory
        if os.path.abspath(local_filepath) != os.path.abspath(destination_path):
            shutil.copy2(local_filepath, destination_path)

        # Also sync to Next.js public/ folder so video can be streamed from frontend server immediately
        try:
            workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            public_dir = os.path.join(workspace_root, "public")
            if os.path.exists(public_dir):
                shutil.copy2(local_filepath, os.path.join(public_dir, destination_filename))
                # Update demo_lesson.mp4 default preview file
                shutil.copy2(local_filepath, os.path.join(public_dir, "demo_lesson.mp4"))
        except Exception as e:
            print("Notice: could not mirror to public/ dir:", e)

        # Return static path accessible via Next.js proxy rewrite or direct API
        return f"/static/{destination_filename}"
