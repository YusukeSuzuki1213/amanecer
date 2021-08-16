from entity.item import Item
from typing import Any, Dict, List


class GetDynamoDbItemsSuccessMapper(object):
    @classmethod
    def to_entity(cls, response: Dict[str, Any]) -> List[Item]:
        return list(
            map(
                lambda item: Item(
                    content_id=item['content_id'],
                    title=item['title'],
                    affiliate_url=item['affiliate_url'],
                    actresses=item['actresses'],
                    genres=list(
                        map(lambda genre: Item.Genre(
                            int(genre['id']), genre['name']), item['genres'])
                    ),
                    image_url=item['image_url'],
                    video_url=item['video_url'],
                    release_date=item['release_date'],
                    article_url=item['article_url']
                ), response['Items']
            )
        )
