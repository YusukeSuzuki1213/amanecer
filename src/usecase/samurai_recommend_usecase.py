from injector import inject
from abc import ABCMeta, abstractmethod
from repository.twitter_repository import AbstractTwitterRepository
from repository.dmm_repository import AbstractDmmRepository
from entity.samurai_recommend_content import SamuraiRecommendContent, RecommendType
from entity.params.twitter_reply_params import ReplyParams
from entity.failure import Failure
from entity.params.get_dmm_items_params import GetDmmItemsParams
from log import SlackClient
from random import choice


class SamuraiRecommendUseCase(metaclass=ABCMeta):
    @inject
    def __init__(self, dmm_repository: AbstractDmmRepository, twitter_repository: AbstractTwitterRepository):
        self.dmm_repository = dmm_repository
        self.twitter_repository = twitter_repository

    @abstractmethod
    def handle(self) -> None:
        pass


class SamuraiRecommendInteractor(SamuraiRecommendUseCase):
    NUMBER_OF_ITEMS_TO_GET = 5

    def handle(self) -> None:
        self.twitter_repository.start_samurai_stream(
            self._after_received
        )

    def _after_received(self, content: SamuraiRecommendContent) -> None:
        params: GetDmmItemsParams

        # Params作成
        if(content.recommend_type.value == RecommendType.POPULAR.value):
            params = GetDmmItemsParams.create_get_popular_item_params(
                hits=self.NUMBER_OF_ITEMS_TO_GET
            )
        elif (content.recommend_type.value == RecommendType.SALE.value):
            # TODO: 別のSALEもあるが。それもとっておきたい。
            params = GetDmmItemsParams.create_get_limited_time_sale_item_params(
                hits=self.NUMBER_OF_ITEMS_TO_GET
            )
        elif(content.recommend_type.value == RecommendType.DEBUT.value):
            params = GetDmmItemsParams.create_get_debut_item_params(
                hits=self.NUMBER_OF_ITEMS_TO_GET
            )
        elif(content.recommend_type.value == RecommendType.KEYWORD.value):
            params = GetDmmItemsParams.create_get_items_by_keyword_params(
                keyword=content.keyword,
                hits=self.NUMBER_OF_ITEMS_TO_GET,
            )
        else:
            return None

        # apiリクエスト
        if isinstance(
            items := self.dmm_repository.get_items(params),
            Failure
        ):
            items.print_failure()
            return None

        # Not Found
        if len(items) == 0:
            SlackClient().send_alert(
                "itemsが取得できませんでした。status_id: {}, screen_name: {}, keyword: {}".format(
                    content.in_reply_to_status_id,
                    content.screen_name,
                    content.keyword
                )
            )
            return None

        # ランダムで取得
        item = choice(items)

        if isinstance(
            reply_result := self.twitter_repository.reply(
                # TODO: itemを渡す
                ReplyParams.create_samurai_recommend_reply_params(
                    item,
                    content
                )
            ),
            Failure
        ):
            reply_result.print_failure()
