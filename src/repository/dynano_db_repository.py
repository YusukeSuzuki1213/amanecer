from abc import ABCMeta, abstractmethod
from entity.params.dynamo_db_update_tweet_id_params import DynamoDbUpdateTweetIdParams
from entity.params.dynamo_db_add_all_params import DynamoDbAddAllParams
from datasource.remote.dynamo_db_api_client import DynamoDbApiClient
from typing import List, Union
from dataclasses import asdict
from botocore.errorfactory import ClientError
from traceback import format_exc
from entity.failure import Failure
from entity.params.dynamo_db_update_article_url_params import DynamoDbUpdateArticleUrlParams


class AbstractDynamoDbRepository(metaclass=ABCMeta):
    @abstractmethod
    def add_all(self, params_list: List[DynamoDbAddAllParams]) -> Union[List[str], Failure]:
        pass

    @abstractmethod
    def update_article_url(self, params: DynamoDbUpdateArticleUrlParams) -> Union[None, Failure]:
        pass

    @abstractmethod
    def update_tweet_id_as_reservation(self, params: DynamoDbUpdateTweetIdParams) -> Union[None, Failure]:
        pass


class DynamoDbRepository(AbstractDynamoDbRepository):
    def __init__(self, dynamo_db_api_client: DynamoDbApiClient) -> None:
        self.dynamo_db_api_client = dynamo_db_api_client

    def add_all(self, params_list: List[DynamoDbAddAllParams]) -> Union[List[str], Failure]:
        stored_item_ids: List[str] = []

        for params in params_list:
            try:
                self.dynamo_db_api_client.put_item(asdict(params))
                stored_item_ids.append(params.content_id)
            except ClientError as e:
                if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                    # すでにdbに保存しようとしたcontent_idが存在したとき
                    continue
                else:
                    return Failure('商品情報をdynamoDBに保存するときにエラー', format_exc())
            except Exception:
                return Failure('商品情報をdynamoDBに取得するときにエラー', format_exc())

        return stored_item_ids

    def update_article_url(self, params: DynamoDbUpdateArticleUrlParams) -> Union[None, Failure]:
        try:
            self.dynamo_db_api_client.update_article_url(params)
        except Exception:
            return Failure('DynamoDbにWordPressへ投稿したデータを保存中にエラー', format_exc())

    def update_tweet_id_as_reservation(self, params: DynamoDbUpdateTweetIdParams) -> Union[None, Failure]:
        try:
            self.dynamo_db_api_client.update_tweet_id_as_reservation(params)
        except Exception:
            return Failure('DynamoDbにtweetのid保存中にエラー', format_exc())
