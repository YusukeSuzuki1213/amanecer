import tweepy
from typing import Any, Callable, List
from tweepy.auth import OAuthHandler
from abc import ABCMeta, abstractmethod
from log import SlackClient


class TwitterStreamClient:

    def __init__(self, consumer_token: str, consumer_secret: str, access_token: str, access_secret: str, stream_listener: 'AbstractTwitterStreamListener', stream_filter_follow: List[str]) -> None:
        self._auth = self._auth_twitter(
            consumer_token, consumer_secret, access_token, access_secret
        )
        self._stream = tweepy.Stream(auth=self._auth, listener=stream_listener)
        self._stream_filter_follow = stream_filter_follow

    def _auth_twitter(self, consumer_token: str, consumer_secret: str, access_token: str, access_secret: str) -> OAuthHandler:
        auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        return auth

    def listen(self, callback: Callable[[Any], None]) -> None:
        self._stream.listener.set_callback(callback)
        self._stream.filter(follow=self._stream_filter_follow, is_async=True)

    def samurai_listen(self, callback: Callable[[Any], None]) -> None:
        self._stream.listener.set_callback(callback)
        self._stream.filter(track=[''], is_async=True)


class AbstractTwitterStreamListener(tweepy.StreamListener, metaclass=ABCMeta):
    @abstractmethod
    def set_callback(self, callback: Callable[[Any], None]) -> None:
        pass


class TwitterStreamListener(AbstractTwitterStreamListener):
    def set_callback(self, callback: Callable[[Any], None]) -> None:
        self._callback = callback

    def on_status(self, status: Any):
        self._callback(status._json)

    # TODO: エラー時の処理
    def on_error(self, status_code: int):
        SlackClient().send_alert(
            "streamlistener on_error status_code: {}".format(status_code)
        )
        if status_code == 420:
            print("Error")
        return False
