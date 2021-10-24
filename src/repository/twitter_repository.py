from abc import ABCMeta, abstractmethod
from entity.params.twitter_tweet_params import TweetParams
from datasource.remote.twitter_api_client import TwitterApiClient
from entity.failure import Failure
from typing import Union, Callable
from traceback import format_exc
from entity.replied_content import RepliedContent
from datasource.remote.twitter_stream_client import TwitterStreamClient


class AbstractTwitterRepository(metaclass=ABCMeta):

    @abstractmethod
    def tweet(self, params: TweetParams) -> Union[int, Failure]:
        pass

    @abstractmethod
    def start_stream(self, callback: Callable[[RepliedContent], None]) -> Union[None, Failure]:
        pass


class TwitterRepository(AbstractTwitterRepository):

    def __init__(self, api_client: TwitterApiClient, stream_client: TwitterStreamClient) -> None:
        self.api_client = api_client
        self.stream_client = stream_client

    def tweet(self, params: TweetParams) -> Union[int, Failure]:
        try:
            response = self.api_client.tweet(params)
            return response.id
        except Exception:
            return Failure('ツイート中にエラー', format_exc())

    def start_stream(self, callback: Callable[[RepliedContent], None]) -> Union[None, Failure]:
        try:
            self.stream_client.listen(
                lambda response:
                    # TODO: mapper実装, callback実行時にNoneチェック
                    callback(
                        RepliedContent(
                            status_id="status_id",
                            url="https://example.com"
                        )
                    )
            )
            return None
        except Exception:
            return Failure('Stream開始時にエラー', format_exc())
