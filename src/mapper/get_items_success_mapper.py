import requests
import re
from entity.item import Item
from typing import Any, Dict, List
from bs4 import BeautifulSoup
from config import (
    DMM_CRAWLER_VIDEO_SERCH_URL, DMM_CRAWLER_URL, DMM_CRAWLER_VIDEO_URL
)


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
                release_date=item['date'].split(' ')[0],
                min_price='¥{}'.format(item['prices']['price']),
            ), items)
        )

    @classmethod
    def __get_video_url(cls, content_id: str) -> str:

        video_search_url = DMM_CRAWLER_VIDEO_SERCH_URL.format(
            content_id
        )
        url = DMM_CRAWLER_URL.format(
            content_id
        )
        try:
            session = requests.Session()
            session.get(video_search_url)
            response = session.get(url)
            soup = BeautifulSoup(response.text, "lxml")
            find_src = soup.find("iframe", allow="autoplay").get("src")
            tcid = re.findall("cid=(.*)/mtype", find_src)[0]

            video_url = DMM_CRAWLER_VIDEO_URL.format(
                tcid[:1], tcid[:3], tcid, tcid)
            return video_url
        except Exception:
            return ''
