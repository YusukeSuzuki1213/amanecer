from traceback import format_exc
from typing import Any, Optional
from entity.reply_to_actress_content import ReplyToActressContent
from log import SlackClient


class GetReplyToActressSuccessMapper(object):

    @classmethod
    def to_entity(cls, response_json: Any) -> Optional['ReplyToActressContent']:
        try:
            if (cls.__should_reply(response_json)):
                print("should reply")
                return ReplyToActressContent(
                    user_id=response_json['user']['id'],
                    tweet_id=response_json['id'],
                    screen_name=response_json['user']['screen_name']
                )
            else:
                print(response_json['id'])
                print("should not reply")
                return None
        except Exception:
            SlackClient().send_alert("Not matched tweet: {}".format(format_exc()))
            return None

    @classmethod
    def __should_reply(cls, res: Any) -> bool:
        is_not_reply = res['in_reply_to_user_id'] is None

        is_not_retweet = ('retweeted_status' not in res) and (
            not res['is_quote_status']
        )

        has_not_url = len(res['entities']['urls']) == 0

        has_media = 'media' in res['entities']

        return is_not_reply and is_not_retweet and has_not_url and has_media
