from dataclasses import dataclass
from entity.item import Item
from typing import List


@dataclass
class ReservationOutputData:
    items_from_dmm_api: List[Item]
    items_stored_dynamo_db: List[Item]
    posted_data: List['PostedData']

    @dataclass
    class PostedData:
        item: Item
        wp_media_id: int
        article_url: str
        tweet_id: int
