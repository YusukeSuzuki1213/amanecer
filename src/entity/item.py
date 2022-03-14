from datetime import datetime
import this
from typing import List
from dataclasses import dataclass, field


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
    campaign: List['Campaign'] = field(default_factory=list)


@dataclass
class Genre:
    id: int
    name: str


@dataclass
class Campaign:
    title: str
    date_begin: str
    date_end: str

    def date_begin_datetime(self) -> datetime:
        return datetime.strptime(self.date_begin, '%Y-%m-%d %H:%M:%S')

    def date_end_datetime(self) -> datetime:
        return datetime.strptime(self.date_end, '%Y-%m-%d %H:%M:%S')
