from input_data.reservation_input_data import ReservationInputData
from usecase.reservation_usecase import ReservationUseCase
from injector import inject


class Controller(object):
    @inject
    def __init__(self, usecase: ReservationUseCase):
        self.usecase = usecase
        pass

    def tweet_reservation_items(self, datetime_iso: str) -> None:
        self.usecase.handle(
            ReservationInputData(datetime_iso)
        )
