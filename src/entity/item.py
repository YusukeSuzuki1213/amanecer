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
    article_url: str = ''

    @dataclass
    class Genre:
        id: int
        name: str
