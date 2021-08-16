import random
from dataclasses import dataclass
from entity.item import Item
from typing import List


@dataclass
class TweetParams:
    message: str

    @classmethod
    def create_reservation_tweet_params(cls, item: Item, article_url: str) -> 'TweetParams':
        return TweetParams(
            ''.join([
                cls.__get_first_sentence(),
                cls.__get_feeling(),
                '' if len(item.actresses) == 0 else cls.__get_actresses(
                    item.actresses),
                cls.__get_guide_sentence(),
                article_url
            ])
        )

    @classmethod
    def create_release_tweet_params(cls, item: Item) -> 'TweetParams':
        return TweetParams(
            'テスト {}'.format(
                item.article_url
            )
        )

    @classmethod
    def __get_first_sentence(cls) -> str:
        return (random.choice(
            [
                '',
                '',
                '',
                '',
            ]) + '\n\n'
        )

    @classmethod
    def __get_feeling(cls) -> str:
        return (random.choice(
            [
                '',
                '',
                '',
                '',
                '',
                '',
            ]) + '\n\n'
        )

    @classmethod
    def __get_actresses(cls, actresses: List[str]) -> str:
        return (' '.join(
            list(
                map(lambda name: '#{}'.format(name), actresses)
            )[:4]) + '\n\n'
        )

    @classmethod
    def __get_guide_sentence(cls) -> str:
        return (random.choice(
            [
                '',
            ]) + '\n'
        )
