from typing import Any
from entity.samurai_recommend_content import SamuraiRecommendContent, RecommendType
from config import TWITTER_SAMURAI_HASH_TAG


class GetSamuraiRecommendSuccessMapper(object):

    @classmethod
    def to_entity(cls, response_json: Any) -> 'SamuraiRecommendContent':
        text = str(response_json['text'])
        recommend_type = cls.__get_recommend_type(text)

        keyword = text.replace('\n', '').replace(TWITTER_SAMURAI_HASH_TAG, '')

        return SamuraiRecommendContent(
            keyword=keyword,
            recommend_type=recommend_type,
            screen_name=response_json['user']['screen_name'],
            in_reply_to_status_id=response_json['id'],
        )

    @classmethod
    def __get_recommend_type(cls, text: str) -> 'RecommendType':
        # 条件を実装
        return RecommendType.KEYWORD
