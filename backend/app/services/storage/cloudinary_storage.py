import os
import cloudinary
import cloudinary.uploader
from app.config import settings
from app.core.providers.storage_base import BaseStorageProvider

class CloudinaryStorageProvider(BaseStorageProvider):
    """
    Cloudinary CDN storage provider.
    Provides global fast streaming, adaptive bitrate HLS transcoding, and signed URLs.
    """

    def __init__(self):
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True,
        )

    async def upload_video(
        self,
        local_filepath: str,
        destination_filename: str,
    ) -> str:
        if not settings.CLOUDINARY_CLOUD_NAME:
            raise ValueError("CLOUDINARY_CLOUD_NAME is not set. Switch to STORAGE_PROVIDER='local' for offline dev.")

        public_id = os.path.splitext(destination_filename)[0]

        upload_result = cloudinary.uploader.upload_large(
            local_filepath,
            resource_type="video",
            folder="chalkka_lessons",
            public_id=public_id,
            overwrite=True,
        )

        return upload_result.get("secure_url", upload_result.get("url", ""))
