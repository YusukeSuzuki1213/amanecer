from abc import ABCMeta, abstractmethod
from entity.params.twitter_tweet_params import TweetParams
from datasource.remote.twitter_api_client import TwitterApiClient
from entity.failure import Failure
from typing import Any, Union, Callable, List
from traceback import format_exc
from entity.replied_content import RepliedContent
from datasource.remote.twitter_stream_client import TwitterStreamClient
from entity.params.twitter_reply_params import ReplyParams
from mapper.get_twitter_reply_success_mapper import GetTwitterReplySuccessMapper
from log import SlackClient
from entity.samurai_recommend_content import SamuraiRecommendContent
from mapper.get_samurai_recommend_success_mapper import GetSamuraiRecommendSuccessMapper
from entity.reply_to_actress_content import ReplyToActressContent
from mapper.get_reply_to_actress_success_mapper import GetReplyToActressSuccessMapper


class AbstractTwitterRepository(metaclass=ABCMeta):

    @abstractmethod
    def tweet(self, params: TweetParams) -> Union[int, Failure]:
        pass

    @abstractmethod
    def reply(self, params: ReplyParams) -> Union[int, Failure]:
        pass

    @abstractmethod
    def start_stream(self, callback: Callable[[RepliedContent], None]) -> None:
        pass

    # TODO: AbstRepositoryを継承した別のsamuraiだけのRepositoryを作成して、start_streamを実装してあげる方が良さそう。
    # Callableの型も抽象化してあげる。
    @abstractmethod
    def start_samurai_stream(self, callback: Callable[[SamuraiRecommendContent], None]) -> None:
        pass

    @abstractmethod
    def start_reply_to_actress_stream(self, follow_list: List[str], callback: Callable[[ReplyToActressContent], None]) -> None:
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

    def reply(self, params: ReplyParams) -> Union[int, Failure]:
        try:
            response = self.api_client.reply(params)
            return response.id
        except Exception:
            SlackClient().send_alert('リプライ中にエラー{}'.format(format_exc()))
            return Failure('リプライ中にエラー', format_exc())

    def start_stream(self, callback: Callable[[RepliedContent], None]) -> None:
        self.stream_client.listen(
            callback=lambda response_json: self.__execute_callback(
                response_json, callback
            )
        )

    def start_samurai_stream(self, callback: Callable[[SamuraiRecommendContent], None]) -> None:
        return self.stream_client.samurai_listen(
            callback=lambda response_json: self.__execute_samurai_callback(
                response_json, callback
            )
        )

    def start_reply_to_actress_stream(self, follow_list: List[str], callback: Callable[[ReplyToActressContent], None]) -> None:
        return self.stream_client.reply_to_actress_listen(
            follow_list,
            lambda response_json: self.__execute_reply_to_actress_callback(
                response_json, callback
            )
        )

    def __execute_callback(self, response_json: Any, callback: Callable[[RepliedContent], None]) -> None:
        reply = GetTwitterReplySuccessMapper.to_entity(response_json)

        if(reply is not None):
            callback(reply)

    def __execute_samurai_callback(self, response_json: Any, callback: Callable[[SamuraiRecommendContent], None]) -> None:
        content = GetSamuraiRecommendSuccessMapper.to_entity(response_json)
        callback(content)

    def __execute_reply_to_actress_callback(self, response_json: Any, callback: Callable[[ReplyToActressContent], None]) -> None:
        reply = GetReplyToActressSuccessMapper.to_entity(response_json)

        if(reply is not None):
            callback(reply)
