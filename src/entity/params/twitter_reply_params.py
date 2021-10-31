from dataclasses import dataclass
from typing import List
from entity.tweet_content import TweetContent
from entity.item import Item
from entity.replied_content import RepliedContent


@dataclass
class ReplyParams:
    message: str
    in_reply_to_status_id: int

    @classmethod
    def create_same_reply_params(cls, item: Item, replied_content: RepliedContent) -> 'ReplyParams':
        return ReplyParams(
            message='{} {}'.format(
                cls.__create_mentioons(replied_content.user_mentions),
                TweetContent.get_reply_message_content(item)
            ),
            in_reply_to_status_id=replied_content.in_reply_to_status_id
        )

    @classmethod
    def __create_mentioons(cls, user_mentions: List[str]) -> str:
        return ' '.join(
            list(
                map(
                    lambda user_name: '@' + user_name,
                    user_mentions
                )
            )
        )
