import re
from traceback import format_exc
from typing import Any, Optional
from urllib.parse import unquote
from entity.replied_content import RepliedContent
from log import SlackClient


class GetTwitterReplySuccessMapper(object):

    MATCH_PATTERN = '.*dmm.*cid=(.*)/'

    @classmethod
    def to_entity(cls, response_json: Any) -> Optional['RepliedContent']:
        try:
            if (cls.__should_reply(response_json)):
                return RepliedContent(
                    in_reply_to_status_id=response_json['in_reply_to_status_id'],
                    user_mentions=list(
                        map(lambda mention: mention['screen_name'],
                            response_json['entities']["user_mentions"])
                    ),
                    dmm_content_id=cls.__get_dmm_content_id(
                        unquote(
                            response_json['entities']['urls'][0]['expanded_url']
                        )
                    )
                )
            else:
                SlackClient().send_alert("should not reply:")
                return None
        except Exception:
            SlackClient().send_alert("Not matched tweet: {}".format(format_exc()))
            return None

    @classmethod
    def __should_reply(cls, res: Any) -> bool:

        is_reply = res['in_reply_to_user_id'] is not None

        is_not_self_reply = res['in_reply_to_user_id'] != res['user']['id']

        is_not_retweet = ('retweeted_status' not in res) and (
            not res['is_quote_status'])

        url = unquote(res['entities']['urls'][0]['expanded_url'])
        is_contain_dmm_url = len(re.findall(cls.MATCH_PATTERN, url)) > 0

        return is_reply and is_not_self_reply and is_not_retweet and is_contain_dmm_url

    @ classmethod
    def __get_dmm_content_id(cls, url: str) -> str:
        matched_list = re.findall(cls.MATCH_PATTERN, url)
        return matched_list[0]
