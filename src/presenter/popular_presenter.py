import json
from abc import ABCMeta, abstractmethod
from output_data.popular_output_data import PopularOutputData
from entity.failure import Failure
from dataclasses import asdict


class AbstractPopularPresenter(metaclass=ABCMeta):
    @abstractmethod
    def output(self, output_data: PopularOutputData) -> None:
        pass

    @abstractmethod
    def output_error(self, failure: Failure) -> None:
        pass


class ConsolePopularPresenter(AbstractPopularPresenter):

    def output(self, output_data: PopularOutputData) -> None:

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
        print('DynamoDBから取得したデータ')
        if (output_data.item_from_dynamo_db is not None):
            print(
                json.dumps(
                    asdict(output_data.item_from_dynamo_db),
                    indent=2,
                    ensure_ascii=False
                )
            )

        print('-'*30)
        print('ツイートID')
        print(output_data.tweet_id)

    def output_error(self, failure: Failure) -> None:
        print('Message: {}'.format(failure.message))
        print('Traceback: {}'.format(failure.traceback))
