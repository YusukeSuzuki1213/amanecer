from injector import inject
from abc import ABCMeta, abstractmethod
from repository.twitter_repository import AbstractTwitterRepository
from repository.dmm_repository import AbstractDmmRepository
from entity.samurai_recommend_content import SamuraiRecommendContent


class SamuraiRecommendUseCase(metaclass=ABCMeta):
    @inject
    def __init__(self, dmm_repository: AbstractDmmRepository, twitter_repository: AbstractTwitterRepository):
        self.dmm_repository = dmm_repository
        self.twitter_repository = twitter_repository

    @abstractmethod
    def handle(self) -> None:
        pass


class SamuraiRecommendInteractor(SamuraiRecommendUseCase):
    def handle(self) -> None:
        self.twitter_repository.start_samurai_stream(
            self._after_received
        )

    def _after_received(self, content: SamuraiRecommendContent) -> None:
        print("hello after received")
