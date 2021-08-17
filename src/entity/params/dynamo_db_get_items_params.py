from dataclasses import dataclass
from datetime import datetime

# TODO: ファイル名がクラス名に揃える


@dataclass
class DynamoDbGetItemsForSpecificReleaseDateParams:
    release_date: str

    @classmethod
    def create_get_items_params(cls, datetime_now: datetime) -> 'DynamoDbGetItemsForSpecificReleaseDateParams':

        return DynamoDbGetItemsForSpecificReleaseDateParams(
            release_date=datetime_now.strftime('%Y-%m-%d')
        )
