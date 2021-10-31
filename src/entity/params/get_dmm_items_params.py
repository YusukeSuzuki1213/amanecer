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
    cid: str
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
            hits='15',
            sort='date',
            cid='',
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
            hits='10',
            sort='date',
            cid='',
            article='genre',
            article_id='3006',
            gte_date=datetime_now.strftime('%Y-%m-%dT00:00:00'),
            lte_date=datetime_now.strftime('%Y-%m-%dT23:59:59'),
            mono_stock='',
            output='json'
        )

    @classmethod
    def create_get_popular_item_params(cls) -> 'GetDmmItemsParams':
        return GetDmmItemsParams(
            site='FANZA',
            service='digital',
            floor='videoa',
            hits='100',
            sort='rank',
            cid='',
            article='genre',
            article_id='3006',
            gte_date='',
            lte_date='',
            mono_stock='',
            output='json'
        )

    @classmethod
    def create_get_limited_time_sale_item_params(cls) -> 'GetDmmItemsParams':
        return GetDmmItemsParams(
            site='FANZA',
            service='digital',
            floor='videoa',
            hits='15',
            sort='rank',
            cid='',
            article='genre',
            article_id='6565',
            gte_date='',
            lte_date='',
            mono_stock='',
            output='json'
        )

    @classmethod
    def create_get_item_by_cid_params(cls, cid: str) -> 'GetDmmItemsParams':
        return GetDmmItemsParams(
            site='FANZA',
            service='digital',
            floor='videoa',
            hits='',
            sort='',
            cid=cid,
            article='',
            article_id='',
            gte_date='',
            lte_date='',
            mono_stock='',
            output='json'
        )
