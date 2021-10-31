from typing import List
from dataclasses import dataclass


@dataclass
class Item:
    content_id: str
    title: str
    affiliate_url: str
    actresses: List[str]
    genres: List['Genre']
    image_url: str
    video_url: str
    release_date: str
    min_price: str
    article_url: str = ''  # TODO: ここに入れるべきではない.別のmodelで

    @dataclass
    class Genre:
        id: int
        name: str
