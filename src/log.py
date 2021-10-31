import requests
from config import (
    SLACK_API_TOKEN,
    SLACK_CHANNEL_NAME_FOR_SEND_LOG
)


# TODO: log送信もアーキテクチャに沿うように
class SlackClient:
    _URL = 'https://slack.com/api/chat.postMessage'

    def __init__(self) -> None:
        self._headers = {'Content-Type': 'application/json'}

    def send_alert(self, message: str) -> None:
        params = {"token": SLACK_API_TOKEN,
                  "channel": SLACK_CHANNEL_NAME_FOR_SEND_LOG, "text": message}

        requests.post(self._URL, headers=self._headers, params=params)
