from abc import ABCMeta, abstractmethod
from datasource.remote.wordpress_api_client import WordPressApiClient
from entity.failure import Failure
from typing import Union
from traceback import format_exc
from entity.params.wordpress_post_article_params import PostArticleToWpParams
from entity.params.wordpress_upload_media_params import UploadMediaToWpParams


class AbstractWordPressRepository(metaclass=ABCMeta):
    @abstractmethod
    def upload_media(self, params: UploadMediaToWpParams) -> Union[int, Failure]:
        pass

    @abstractmethod
    def post(self, params: PostArticleToWpParams) -> Union[str, Failure]:
        pass


class WordPressRepository(AbstractWordPressRepository):
    def __init__(self, wordpress_api_client: WordPressApiClient) -> None:
        self.wordpress_api_client = wordpress_api_client

    def upload_media(self, params: UploadMediaToWpParams) -> Union[int, Failure]:
        try:
            resposne = self.wordpress_api_client.upload_media(params)
            return resposne['id']  # entityに変換した方が良いかも
        except Exception:
            return Failure('WordPressにメディアをアップローッド中にエラー', format_exc())

    def post(self, params: PostArticleToWpParams) -> Union[str, Failure]:
        try:
            response = self.wordpress_api_client.post(params)
            return response['link']  # entityに変換した方が良いかも
        except Exception:
            return Failure('WordPressに記事をアップローッド中にエラー', format_exc())
