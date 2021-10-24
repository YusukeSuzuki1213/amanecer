from injector import inject
from repository.twitter_repository import AbstractTwitterRepository
from repository.dmm_repository import AbstractDmmRepository
from abc import ABCMeta, abstractmethod

from entity.failure import Failure
from entity.replied_content import RepliedContent


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

        if isinstance(
            stream_result := self.twitter_repository.start_stream(
                self._after_received
            ),
            Failure
        ):
            # TODO: 本来はpresenterを呼ぶべき
            stream_result.print_failure()
            return None

        return None

    def _after_received(self, replied_content: RepliedContent) -> None:
        print("TODO: dmm APIを叩く")
        print("TODO: same replyする")
