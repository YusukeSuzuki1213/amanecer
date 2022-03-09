from dataclasses import dataclass


@dataclass
class ReplyToActressContent:
    user_id: int
    tweet_id: int
    screen_name: str
