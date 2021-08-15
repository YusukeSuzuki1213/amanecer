import requests
from entity.params.wordpress_post_article_params import PostArticleToWpParams
from entity.params.wordpress_upload_media_params import UploadMediaToWpParams
from typing import Dict, Any
from urllib.request import urlopen
from io import BytesIO


class WordPressApiClient:

    def __init__(self, url: str, user: str, password: str):
        self.url = url
        self.user = user
        self.password = password

    def __request(
        self,
        resource_name: str,
        headers: Dict[str, Any] = {},
        payload: Dict[str, Any] = {},
        data: bytes = bytes(b'')
    ) -> Any:
        response = requests.post(
            self.url + resource_name,
            headers=headers,
            json=payload,
            data=data,
            auth=(self.user, self.password)
        )
        response.raise_for_status()
        return response.json()

    def upload_media(self, params: UploadMediaToWpParams) -> Any:

        data = BytesIO(
            urlopen(params.image_url).read()
        ).getvalue()

        headers = {
            'Content-Type': 'image/jpeg',
            'Content-Disposition': 'attachiment; filename={}'.format(params.file_name)
        }

        return self.__request(
            resource_name=params.resource_name,
            headers=headers,
            data=data
        )

    def post(self, params: PostArticleToWpParams) -> Any:
        payload = {
            'title': params.title,
            'content': params.content,
            'slug': params.slug,
            'categories': params.category_ids,
            'tags': params.tag_ids,
            'featured_media': params.featured_media_id,
            'status': params.status
        }

        return self.__request(
            resource_name=params.resource_name,
            payload=payload,
        )
