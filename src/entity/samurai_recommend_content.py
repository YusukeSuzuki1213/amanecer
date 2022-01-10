from dataclasses import dataclass
from enum import Enum


@dataclass
class SamuraiRecommendContent:
    recommend_type: 'RecommendType'
    screen_name: str
    in_reply_to_status_id: int  # 返信するツイートのID
    keyword: str  # ユーザがツイートしたキーワード


class RecommendType(Enum):
    POPULAR = 'popular'
    SALE = 'sale'
    DEBUT = 'debut'
    KEYWORD = 'keyword'
