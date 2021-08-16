import requests
import re
from entity.item import Item
from typing import Any, Dict, List
from bs4 import BeautifulSoup


class GetItemsSuccessMapper(object):
    @classmethod
    def to_entity(cls, response: Dict[str, Any]) -> List[Item]:
        items = response['result']['items']

        return list(
            map(lambda item: Item(
                content_id=item['content_id'],
                title=item['title'],
                affiliate_url=item['affiliateURL'],
                actresses=list(
                    map(lambda actress: actress['name'],
                        item['iteminfo']['actress'] if 'actress' in item['iteminfo'] else [])
                ),
                genres=list(
                    map(lambda genre: Item.Genre(
                        id=genre['id'],
                        name=genre['name']
                    ), item['iteminfo']['genre'] if 'genre' in item['iteminfo'] else [])
                ),
                image_url=item['imageURL']['large'],
                video_url=cls.__get_video_url(item['content_id']),
                release_date=item['date'].split(' ')[0]
            ), items)
        )

    @classmethod
    def __get_video_url(cls, content_id: str) -> str:
        try:
            return 'https://res.cloudinary.com/code-kitchen/video/upload/v1555082747/movie.mp4'
        except Exception:
            return ''
