from abc import ABC, abstractmethod

class BaseStorageProvider(ABC):
    """
    Abstract Base Class for Video Storage and CDN delivery.
    Enables swapping between Cloudinary, Supabase Storage, Local filesystem, or S3.
    """

    @abstractmethod
    async def upload_video(
        self,
        local_filepath: str,
        destination_filename: str,
    ) -> str:
        """
        Upload final stitched MP4 and return a signed URL, public URL, or CDN stream URL.
        """
        pass
