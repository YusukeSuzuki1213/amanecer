from dataclasses import dataclass
from entity.item import Item


@dataclass
class DynamoDbUpdateArticleUrlParams:
    content_id: str
    article_url: str

    @classmethod
    def create_update_article_url_params(cls, item: Item, article_url: str) -> 'DynamoDbUpdateArticleUrlParams':
        return DynamoDbUpdateArticleUrlParams(
            content_id=item.content_id,
            article_url=article_url
        )
