from dataclasses import dataclass
from entity.item import Item
from typing import List, Union


@dataclass
class PopularOutputData:
    items_from_dmm_api: List[Item]
    items_stored_dynamo_db: List[Item]
    item_from_dynamo_db: Union[Item, None]
    tweet_id: Union[int, None]
