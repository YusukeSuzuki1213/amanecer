from injector import inject
from repository.twitter_repository import AbstractTwitterRepository
from repository.dmm_repository import AbstractDmmRepository
from abc import ABCMeta, abstractmethod

from entity.failure import Failure
from entity.replied_content import RepliedContent
from entity.params.twitter_reply_params import ReplyParams
from entity.params.get_dmm_items_params import GetDmmItemsParams
from log import SlackClient


class SameReplyUseCase(metaclass=ABCMeta):
    @inject
    def __init__(self, dmm_repository: AbstractDmmRepository, twitter_repository: AbstractTwitterRepository):
        self.dmm_repository = dmm_repository
        self.twitter_repository = twitter_repository

    @abstractmethod
    def handle(self) -> None:
        pass


class SameReplyInteractor(SameReplyUseCase):
    def handle(self) -> None:
        self.twitter_repository.start_stream(
            self._after_received
        )

    def _after_received(self, replied_content: RepliedContent) -> None:
        if isinstance(
            items := self.dmm_repository.get_items(
                GetDmmItemsParams.create_get_item_by_cid_params(
                    replied_content.dmm_content_id
                )
            ),
            Failure
        ):
            items.print_failure()
            return None

        if len(items) == 0:
            SlackClient().send_alert("cidをもとにitemが取得できませんでした")
            return None

        if isinstance(
            reply_result := self.twitter_repository.reply(
                ReplyParams.create_same_reply_params(items[0], replied_content)
            ),
            Failure
        ):
            reply_result.print_failure()
