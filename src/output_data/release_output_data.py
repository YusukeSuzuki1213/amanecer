from dataclasses import dataclass
from entity.item import Item
from typing import List


@dataclass
class ReleaseOutputData:
    items_from_dmm_api: List[Item]
    items_stored_dynamo_db: List[Item]
    items_from_dynamo_db: List[Item]
    posted_data: List['PostedData']

    @dataclass
    class PostedData:
        item: Item
        tweet_id: int
