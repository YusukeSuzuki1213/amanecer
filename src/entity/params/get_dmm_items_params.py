from dataclasses import dataclass
from datetime import datetime
from config import DMM_AFFILIATE_ID, DMM_API_KEY, DMM_GET_ITEMS_URL


@dataclass
class GetDmmItemsParams:
    site: str
    service: str
    floor: str
    hits: str
    sort: str
    article: str
    article_id: str
    gte_date: str
    lte_date: str
    mono_stock: str
    output: str
    url: str = DMM_GET_ITEMS_URL
    api_id: str = DMM_API_KEY
    affiliate_id: str = DMM_AFFILIATE_ID

    @classmethod
    def create_get_reservation_item_params(cls, datetime_now: datetime) -> 'GetDmmItemsParams':
        return GetDmmItemsParams(
            site='FANZA',
            service='digital',
            floor='videoa',
            hits='3',
            sort='date',
            article='genre',
            article_id='3006',
            gte_date=datetime_now.replace(microsecond=0).isoformat(),
            lte_date='',
            mono_stock='reserve',
            output='json'
        )

    @classmethod
    def create_get_release_item_params(cls, datetime_now: datetime) -> 'GetDmmItemsParams':
        return GetDmmItemsParams(
            site='FANZA',
            service='digital',
            floor='videoa',
            hits='20',
            sort='date',
            article='genre',
            article_id='3006',
            gte_date=datetime_now.strftime('%Y-%m-%dT00:00:00'),
            lte_date=datetime_now.strftime('%Y-%m-%dT23:59:59'),
            mono_stock='',
            output='json'
        )
