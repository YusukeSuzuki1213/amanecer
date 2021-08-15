from dataclasses import dataclass
from entity.item import Item


@dataclass
class DynamoDbUpdateTweetIdParams:
    content_id: str
    tweet_id: int

    @classmethod
    def create_update_tweet_id_params(cls, item: Item, tweet_id: int) -> 'DynamoDbUpdateTweetIdParams':
        return DynamoDbUpdateTweetIdParams(
            content_id=item.content_id,
            tweet_id=tweet_id
        )
