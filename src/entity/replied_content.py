from dataclasses import dataclass
from typing import List


@dataclass
class RepliedContent:
    in_reply_to_status_id: int
    user_mentions: List[str]
    dmm_content_id: str
