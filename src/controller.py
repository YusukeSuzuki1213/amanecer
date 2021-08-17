from datetime import datetime
from usecase.popular_usecase import PopularUseCase
from input_data.release_input_data import ReleaseInputData
from usecase.release_usecase import ReleaseUseCase
from input_data.reservation_input_data import ReservationInputData
from usecase.reservation_usecase import ReservationUseCase
from injector import inject
from input_data.popular_input_data import PopularInputData


class Controller(object):
    @inject
    def __init__(self, reservation_usecase: ReservationUseCase, release_usecase: ReleaseUseCase, popular_usecase: PopularUseCase):
        self.reservation_usecase = reservation_usecase
        self.release_usecase = release_usecase
        self.popular_usecase = popular_usecase
        pass

    def tweet_reservation_items(self, datetime_now: datetime) -> None:
        self.reservation_usecase.handle(
            ReservationInputData(datetime_now)
        )

    def tweet_release_items(self, datetime_now: datetime) -> None:
        return self.release_usecase.handle(
            ReleaseInputData(
                datetime_now
            )
        )

    def tweet_popular_items(self, datetime_now: datetime) -> None:
        return self.popular_usecase.handle(
            PopularInputData(
                datetime_now
            )
        )
