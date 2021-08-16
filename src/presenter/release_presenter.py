import json
from abc import ABCMeta, abstractmethod
from output_data.release_output_data import ReleaseOutputData
from entity.failure import Failure
from dataclasses import asdict


class AbstractReleasePresenter(metaclass=ABCMeta):
    @abstractmethod
    def output(self, output_data: ReleaseOutputData) -> None:
        pass

    @abstractmethod
    def output_error(self, failure: Failure) -> None:
        pass


class ConsoleReleasePresenter(AbstractReleasePresenter):

    def output(self, output_data: ReleaseOutputData) -> None:
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
        print('DynamoDBから取得したデータ')
        for item in output_data.items_from_dynamo_db:
            print(
                json.dumps(
                    asdict(item),
                    indent=2,
                    ensure_ascii=False
                )
            )

        print('-'*30)
        print('Twitterに投稿したデータ')
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
