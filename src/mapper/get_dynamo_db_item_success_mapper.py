from entity.item import Item
from typing import Any, Dict, List, Union


class GetDynamoDbItemsSuccessMapper(object):
    @classmethod
    def to_entity_list(cls, response: Dict[str, Any]) -> List[Item]:
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
                    article_url=item['article_url'],
                    min_price=item['min_price'],
                ), response['Items']
            )
        )

    @classmethod
    def to_entity(cls, response: Dict[str, Any]) -> Union[Item, None]:
        item = response['Items'][:1]

        if len(item) == 0:
            return None

        return Item(
            content_id=item[0]['content_id'],
            title=item[0]['title'],
            affiliate_url=item[0]['affiliate_url'],
            actresses=item[0]['actresses'],
            genres=list(
                map(lambda genre: Item.Genre(
                    int(genre['id']), genre['name']), item[0]['genres'])
            ),
            image_url=item[0]['image_url'],
            video_url=item[0]['video_url'],
            release_date=item[0]['release_date'],
            article_url=item[0]['article_url'],
            min_price=item[0]['min_price'],
        )
