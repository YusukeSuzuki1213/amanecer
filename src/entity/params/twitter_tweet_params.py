from dataclasses import dataclass
from entity.tweet_content import TweetContent
from entity.item import Item


@dataclass
class TweetParams:
    message: str

    @classmethod
    def create_reservation_tweet_params(cls, item: Item, article_url: str) -> 'TweetParams':
        return TweetParams(
            TweetContent.get_reservation_tweet_content(item, article_url)
        )

    @classmethod
    def create_release_tweet_params(cls, item: Item) -> 'TweetParams':
        return TweetParams(
            TweetContent.get_release_tweet_content(item)
        )

    @classmethod
    def create_popular_tweet_params(cls, item: Item) -> 'TweetParams':
        return TweetParams(
            TweetContent.get_popular_tweet_content(item)
        )
