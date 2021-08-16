from datetime import datetime
from input_data.release_input_data import ReleaseInputData
from usecase.release_usecase import ReleaseUseCase
from input_data.reservation_input_data import ReservationInputData
from usecase.reservation_usecase import ReservationUseCase
from injector import inject


class Controller(object):
    @inject
    def __init__(self, reservation_usecase: ReservationUseCase, release_usecase: ReleaseUseCase):
        self.reservation_usecase = reservation_usecase
        self.release_usecase = release_usecase
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
