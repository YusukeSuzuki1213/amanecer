from abc import ABCMeta, abstractmethod
from entity.params.twitter_tweet_params import TweetParams
from datasource.remote.twitter_api_client import TwitterApiClient
from entity.failure import Failure
from typing import Union
from traceback import format_exc


class AbstractTwitterRepository(metaclass=ABCMeta):
    @abstractmethod
    def tweet(self, params: TweetParams) -> Union[int, Failure]:
        pass


class TwitterRepository(AbstractTwitterRepository):
    def __init__(self, api_client: TwitterApiClient) -> None:
        self.api_client = api_client

    def tweet(self, params: TweetParams) -> Union[int, Failure]:
        try:
            response = self.api_client.tweet(params)
            return response.id
        except Exception:
            return Failure('ツイート中にエラー', format_exc())
