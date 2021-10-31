import tweepy
from typing import Any
from tweepy.auth import OAuthHandler
from entity.params.twitter_tweet_params import TweetParams
from entity.params.twitter_reply_params import ReplyParams


class TwitterApiClient(object):
    def __init__(self, consumer_token: str, consumer_secret: str, access_token: str, access_secret: str) -> None:
        self._auth = self._auth_twitter(
            consumer_token, consumer_secret, access_token, access_secret)
        self._api = tweepy.API(self._auth)

    def _auth_twitter(self, consumer_token: str, consumer_secret: str, access_token: str, access_secret: str) -> OAuthHandler:
        auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        return auth

    def tweet(self, params: TweetParams) -> Any:
        return self._api.update_status(
            params.message
        )

    def reply(self, params: ReplyParams) -> Any:
        return self._api.update_status(
            status=params.message,
            in_reply_to_status_id=params.in_reply_to_status_id
        )

    def get_tweet_by_status_id(self, id: int) -> Any:
        return self._api.get_status(
            id
        )
