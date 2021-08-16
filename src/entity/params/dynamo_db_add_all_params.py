from dataclasses import dataclass
from datetime import datetime
from typing import List
from entity.item import Item


@dataclass
class DynamoDbAddAllParams:
    content_id: str
    title: str
    affiliate_url: str
    actresses: List[str]
    genres: List['Genre']
    image_url: str
    video_url: str
    release_date: str
    created_at: str
    updated_at: str

    @dataclass
    class Genre:
        id: int
        name: str

    @classmethod
    def create_dynamo_db_add_all_params_list(cls, items: List[Item], datetime_now: datetime) -> List['DynamoDbAddAllParams']:
        return list(
            map(lambda item: DynamoDbAddAllParams(
                content_id=item.content_id,
                title=item.title,
                affiliate_url=item.affiliate_url,
                actresses=item.actresses,
                genres=list(
                    map(lambda genre: DynamoDbAddAllParams.Genre(
                        genre.id, genre.name), item.genres)
                ),
                image_url=item.image_url,
                video_url=item.video_url,
                release_date=item.release_date,
                created_at=datetime_now.replace(microsecond=0).isoformat(),
                updated_at=datetime_now.replace(microsecond=0).isoformat(),
            ), list(
                filter(lambda item: item.video_url, items)
            ))
        )
