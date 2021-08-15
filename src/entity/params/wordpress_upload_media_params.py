from dataclasses import dataclass
from config import WP_RESOURCE_NAME_MEDIA


@dataclass
class UploadMediaToWpParams:
    image_url: str
    file_name: str
    resource_name: str = WP_RESOURCE_NAME_MEDIA

    @classmethod
    def create_upload_media_params(cls, content_id: str, image_url: str) -> 'UploadMediaToWpParams':
        return UploadMediaToWpParams(
            image_url=image_url,
            file_name='{}.jpg'.format(content_id)
        )
