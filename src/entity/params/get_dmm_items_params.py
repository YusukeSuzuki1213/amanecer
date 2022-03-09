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
    keyword: str
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
            keyword='',
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
            keyword='',
            cid='',
            article='genre',
            article_id='3006',
            gte_date=datetime_now.strftime('%Y-%m-%dT00:00:00'),
            lte_date=datetime_now.strftime('%Y-%m-%dT23:59:59'),
            mono_stock='',
            output='json'
        )

    @classmethod
    def create_get_popular_3006_genre_item_params(cls) -> 'GetDmmItemsParams':
        return GetDmmItemsParams(
            site='FANZA',
            service='digital',
            floor='videoa',
            hits='100',
            sort='rank',
            keyword='',
            cid='',
            article='genre',
            article_id='3006',
            gte_date='',
            lte_date='',
            mono_stock='',
            output='json'
        )

    @classmethod
    def create_get_limited_time_sale_item_params(cls, hits: int = 15) -> 'GetDmmItemsParams':
        return GetDmmItemsParams(
            site='FANZA',
            service='digital',
            floor='videoa',
            hits=str(hits),
            sort='rank',
            keyword='',
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
            keyword='',
            cid=cid,
            article='',
            article_id='',
            gte_date='',
            lte_date='',
            mono_stock='',
            output='json'
        )

    @classmethod
    def create_get_popular_item_params(cls, hits: int = 15) -> 'GetDmmItemsParams':
        return GetDmmItemsParams(
            site='FANZA',
            service='digital',
            floor='videoa',
            hits=str(hits),
            sort='rank',
            keyword='',
            cid='',
            article='',
            article_id='',
            gte_date='',
            lte_date='',
            mono_stock='',
            output='json'
        )

    @classmethod
    def create_get_debut_item_params(cls, hits: int = 15) -> 'GetDmmItemsParams':
        return GetDmmItemsParams(
            site='FANZA',
            service='digital',
            floor='videoa',
            hits=str(hits),
            sort='rank',
            keyword='',
            cid='',
            article='genre',
            article_id='6006',
            gte_date='',
            lte_date='',
            mono_stock='',
            output='json'
        )

    @classmethod
    def create_get_items_by_keyword_params(cls, keyword: str, hits: int = 15) -> 'GetDmmItemsParams':
        return GetDmmItemsParams(
            site='FANZA',
            service='digital',
            floor='videoa',
            hits=str(hits),
            sort='rank',
            keyword=keyword,
            cid='',
            article='',
            article_id='',
            gte_date='',
            lte_date='',
            mono_stock='',
            output='json'
        )

    @classmethod
    def create_get_items_by_actress_id_params(cls, actress_id: int, hits: int = 15) -> 'GetDmmItemsParams':
        return GetDmmItemsParams(
            site='FANZA',
            service='digital',
            floor='videoa',
            hits=str(hits),
            sort='rank',
            keyword='',
            cid='',
            article='actress',
            article_id=str(actress_id),
            gte_date='',
            lte_date='',
            mono_stock='',
            output='json'
        )
