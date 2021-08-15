from dataclasses import dataclass
from entity.item import Item
from typing import List
from config import WP_RESOURCE_NAME_POST, WP_COTEGORY_ID


@dataclass
class PostArticleToWpParams:
    title: str
    content: str
    slug: str
    tag_ids: List[int]
    featured_media_id: int
    status: str
    category_ids: List[int]
    resource_name: str = WP_RESOURCE_NAME_POST

    @classmethod
    def create_post_article_params(cls, item: Item, media_id: int) -> 'PostArticleToWpParams':
        return PostArticleToWpParams(
            title='{}'.format(item.title),
            content='{}{}{}'.format(
                item.image_url, item.video_url, item.affiliate_url
            ),
            slug=item.content_id,
            tag_ids=[],  # タグは一旦なし
            featured_media_id=media_id,
            status='publish',
            category_ids=[WP_COTEGORY_ID]  # TODO: dataclassのデフォルト値とするべき
        )
