from entity.params.dynamo_db_get_items_params import DynamoDbGetItemsForSpecificReleaseDateParams
from entity.params.dynamo_db_update_tweet_id_params import DynamoDbUpdateTweetIdParams
from boto3.session import Session
from typing import Dict, Any
from entity.params.dynamo_db_update_article_url_params import DynamoDbUpdateArticleUrlParams
from boto3.dynamodb.conditions import Attr, Key


class DynamoDbApiClient():
    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, regin_name: str, table_name: str) -> None:
        self.session = Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=regin_name
        )
        self.dynamo_db = self.session.resource('dynamodb')
        self.table = self.dynamo_db.Table(table_name)

    def put_item(self, item: Dict[str, Any]) -> None:
        self.table.put_item(
            Item=item,
            ConditionExpression='attribute_not_exists(content_id)'
        )

    def update_article_url(self, params: DynamoDbUpdateArticleUrlParams) -> None:
        self.table.update_item(
            Key={
                'content_id': params.content_id,
            },
            ExpressionAttributeNames={
                '#article_url': 'article_url'
            },
            ExpressionAttributeValues={
                ':article_url': params.article_url,
            },
            UpdateExpression="set #article_url=:article_url",
        )

    def update_tweet_id_as_reservation(self, params: DynamoDbUpdateTweetIdParams) -> None:
        self.table.update_item(
            Key={
                'content_id': params.content_id,
            },
            ExpressionAttributeNames={
                '#tweet_id_as_reservation': 'tweet_id_as_reservation'
            },
            ExpressionAttributeValues={
                ':tweet_id_as_reservation': params.tweet_id
            },
            UpdateExpression="set #tweet_id_as_reservation=:tweet_id_as_reservation",
        )

    def get_items_for_specific_release_date(self, params: DynamoDbGetItemsForSpecificReleaseDateParams) -> Dict[str, Any]:
        return self.table.query(
            IndexName='release_date-index',
            KeyConditionExpression=Key(
                'release_date').eq(params.release_date),
            FilterExpression=Attr('tweet_id_as_release').not_exists() & Attr(
                'article_url').exists()
        )

    def update_tweet_id_as_release(self, params: DynamoDbUpdateTweetIdParams) -> None:
        self.table.update_item(
            Key={
                'content_id': params.content_id,
            },
            ExpressionAttributeNames={
                '#tweet_id_as_release': 'tweet_id_as_release'
            },
            ExpressionAttributeValues={
                ':tweet_id_as_release': params.tweet_id
            },
            UpdateExpression="set #tweet_id_as_release=:tweet_id_as_release",
        )
