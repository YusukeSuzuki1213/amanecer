import json
from abc import ABCMeta, abstractmethod
from output_data.reservation_output_data import ReservationOutputData
from entity.failure import Failure
from dataclasses import asdict


class AbstractReservationPresenter(metaclass=ABCMeta):
    @abstractmethod
    def output(self, output_data: ReservationOutputData) -> None:
        pass

    @abstractmethod
    def output_error(self, failure: Failure) -> None:
        pass


class ConsoleReservationPresenter(AbstractReservationPresenter):

    def output(self, output_data: ReservationOutputData) -> None:
        # 本来はviewで処理すべき
        print('-'*30)
        print('DMM APIから取得したデータ')
        for item in output_data.items_from_dmm_api:
            print(
                json.dumps(
                    asdict(item),
                    indent=2,
                    ensure_ascii=False
                )
            )

        print('-'*30)
        print('DynamoDBに新しく保存したデータ')
        for item in output_data.items_stored_dynamo_db:
            print(
                json.dumps(
                    asdict(item),
                    indent=2,
                    ensure_ascii=False
                )
            )

        print('-'*30)
        print('WordPressやツイッターにポストしたデータ')
        for data in output_data.posted_data:
            print(
                json.dumps(
                    asdict(data),
                    indent=2,
                    ensure_ascii=False
                )
            )

        print('-'*30)

    def output_error(self, failure: Failure) -> None:
        print('Message: {}'.format(failure.message))
        print('Traceback: {}'.format(failure.traceback))
