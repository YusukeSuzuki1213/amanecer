from abc import ABCMeta, abstractmethod
from mapper.get_dynamo_db_item_success_mapper import GetDynamoDbItemsSuccessMapper
from entity.params.dynamo_db_get_items_params import DynamoDbGetItemsForSpecificReleaseDateParams
from entity.item import Item
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

    @abstractmethod
    def get_items_for_specific_release_date(self, params: DynamoDbGetItemsForSpecificReleaseDateParams) -> Union[List[Item], Failure]:
        pass

    @abstractmethod
    def update_tweet_id_as_release(self, params: DynamoDbUpdateTweetIdParams) -> Union[None, Failure]:
        pass

    @abstractmethod
    def get_popular_item(self) -> Union[Union[Item, None], Failure]:
        pass

    @abstractmethod
    def update_tweet_id_as_popular(self, params: DynamoDbUpdateTweetIdParams) -> Union[None, Failure]:
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
                    # ?????????db???????????????????????????content_id?????????????????????
                    continue
                else:
                    return Failure('???????????????dynamoDB?????????????????????????????????', format_exc())
            except Exception:
                return Failure('???????????????dynamoDB?????????????????????????????????', format_exc())

        return stored_item_ids

    def update_article_url(self, params: DynamoDbUpdateArticleUrlParams) -> Union[None, Failure]:
        try:
            self.dynamo_db_api_client.update_article_url(params)
        except Exception:
            return Failure('DynamoDb???WordPress????????????????????????????????????????????????', format_exc())

    def update_tweet_id_as_reservation(self, params: DynamoDbUpdateTweetIdParams) -> Union[None, Failure]:
        try:
            self.dynamo_db_api_client.update_tweet_id_as_reservation(params)
        except Exception:
            return Failure('DynamoDb???tweet???id?????????????????????', format_exc())

    def get_items_for_specific_release_date(self, params: DynamoDbGetItemsForSpecificReleaseDateParams) -> Union[List[Item], Failure]:
        try:
            response = self.dynamo_db_api_client.get_items_for_specific_release_date(
                params)
            return GetDynamoDbItemsSuccessMapper.to_entity_list(response)
        except Exception:
            return Failure('DynamoDb???????????????????????????', format_exc())

    def update_tweet_id_as_release(self, params: DynamoDbUpdateTweetIdParams) -> Union[None, Failure]:
        try:
            self.dynamo_db_api_client.update_tweet_id_as_release(params)
        except Exception:
            return Failure('DynamoDb???tweet???id?????????????????????', format_exc())

    def get_popular_item(self) -> Union[Union[Item, None], Failure]:
        try:
            response = self.dynamo_db_api_client.get_popular_item()
            return GetDynamoDbItemsSuccessMapper.to_entity(response)
        except Exception:
            return Failure('DynamoDB???????????????????????????')

    def update_tweet_id_as_popular(self, params: DynamoDbUpdateTweetIdParams) -> Union[None, Failure]:
        try:
            self.dynamo_db_api_client.update_tweet_id_as_popular(params)
        except Exception:
            return Failure('DynamoDb???tweet???id?????????????????????', format_exc())
