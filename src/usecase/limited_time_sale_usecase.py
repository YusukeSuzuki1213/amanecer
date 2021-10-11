from entity.failure import Failure
from entity.item import Item
from entity.params.get_dmm_items_params import GetDmmItemsParams
from repository.twitter_repository import AbstractTwitterRepository
from repository.dmm_repository import AbstractDmmRepository
from injector import inject
from abc import ABCMeta, abstractmethod
from typing import List
from random import choice
from entity.params.twitter_tweet_params import TweetParams


class LimitedTimeSaleUseCase(metaclass=ABCMeta):
    @inject
    def __init__(self, dmm_repository: AbstractDmmRepository, twitter_repository: AbstractTwitterRepository):
        self.dmm_repository = dmm_repository
        self.twitter_repository = twitter_repository

    @abstractmethod
    def handle(self) -> None:
        pass


class LimitedTimeSaleInteractor(LimitedTimeSaleUseCase):
    def handle(self) -> None:

        # DMM APIから商品取得
        if isinstance(items := self.dmm_repository.get_items(
            GetDmmItemsParams.create_get_limited_time_sale_item_params()
        ), Failure):
            # TODO: presenterへ
            return None

        item = self.__get_tweet_item(items)

        # ツイート
        if isinstance(self.twitter_repository.tweet(
            TweetParams.create_limited_time_sale_tweet_params(item)
        ), Failure):
            # TODO: presenterへ
            return None

        # TODO: presenterへ
        return None

    # ツイートするアイテムをランダムで取得
    def __get_tweet_item(self, items: List[Item]) -> Item:
        return choice(items)
