from datetime import datetime
from usecase.same_reply_usecase import SameReplyUseCase
from usecase.limited_time_sale_usecase import LimitedTimeSaleUseCase
from usecase.popular_usecase import PopularUseCase
from input_data.release_input_data import ReleaseInputData
from usecase.release_usecase import ReleaseUseCase
from input_data.reservation_input_data import ReservationInputData
from usecase.reservation_usecase import ReservationUseCase
from injector import inject
from input_data.popular_input_data import PopularInputData


class Controller(object):
    @inject
    def __init__(self, reservation_usecase: ReservationUseCase, release_usecase: ReleaseUseCase, popular_usecase: PopularUseCase, limited_time_sale_usecase: LimitedTimeSaleUseCase, same_reply_usecase: SameReplyUseCase):
        self.reservation_usecase = reservation_usecase
        self.release_usecase = release_usecase
        self.popular_usecase = popular_usecase
        self.limited_time_sale_usecase = limited_time_sale_usecase
        self.same_reply_usecase = same_reply_usecase
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

    def tweet_limited_time_sale_item(self) -> None:
        return self.limited_time_sale_usecase.handle()

    def tweet_same_reply(self) -> None:
        return self.same_reply_usecase.handle()
