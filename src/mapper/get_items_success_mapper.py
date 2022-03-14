import requests
import re
import datetime
from entity.item import Item, Genre, Campaign
from typing import Any, Dict, List, Optional
from bs4 import BeautifulSoup
from config import (
    DMM_CRAWLER_VIDEO_SERCH_URL, DMM_CRAWLER_URL, DMM_CRAWLER_VIDEO_URL
)
from log import SlackClient


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
                    map(lambda genre: Genre(
                        id=genre['id'],
                        name=genre['name']
                    ), item['iteminfo']['genre'] if 'genre' in item['iteminfo'] else [])
                ),
                image_url=item['imageURL']['large'],
                video_url=cls.__get_video_url(item['content_id']),
                release_date=item['date'].split(' ')[0],
                min_price='¥{}'.format(item['prices']['price']),
                campaign=cls.__get_campaign(item),
            ), items)
        )

    @classmethod
    def __get_campaign(cls, item: Any) -> List['Campaign']:
        if 'campaign' not in item:
            return []

        try:
            dt_now = datetime.datetime.now()
            return list(
                filter(
                    lambda campaign: campaign.date_begin_datetime() < dt_now and dt_now < campaign.date_end_datetime() and (
                        "セール" in campaign.title or "OFF" in campaign.title),
                    map(
                        lambda campaign: Campaign(
                            title=campaign['title'],
                            date_begin=campaign['date_begin'],
                            date_end=campaign['date_end'],
                        ),
                        item['campaign']
                    )
                )
            )
        except Exception as e:
            SlackClient().send_alert(
                "Error at campaign response parse: {}\n{}".format(
                    item['campaign'], e)
            )
            return []

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
