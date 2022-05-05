import datetime
import random
from typing import List
from injector import inject
from repository.twitter_repository import AbstractTwitterRepository
from repository.dmm_repository import AbstractDmmRepository
from abc import ABCMeta, abstractmethod
from entity.params.get_dmm_items_params import GetDmmItemsParams
from entity.reply_to_actress_content import ReplyToActressContent
from entity.failure import Failure
from log import SlackClient
from entity.reply_to_actress_follow_list import get_dmm_id_by_twitter_id
from entity.reply_to_actress_follow_list import get_follow_list
from dataclasses import asdict
import boto3
import json
from entity.item import Item
from config import AWS_ACCESS_KEY_ID, AWS_REGIN_NAME, AWS_SECRET_KEY, AWS_QUEUE_URL


class ReplyToActressUseCase(metaclass=ABCMeta):
    @inject
    def __init__(self, dmm_repository: AbstractDmmRepository, twitter_repository: AbstractTwitterRepository):
        self.dmm_repository = dmm_repository
        self.twitter_repository = twitter_repository

    @abstractmethod
    def handle(self) -> None:
        pass


class ReplyToActressInteractor(ReplyToActressUseCase):
    def handle(self) -> None:
        # TODO: Repositoryからfollow_listを取ってくる
        follow_list = get_follow_list()

        self.twitter_repository.start_reply_to_actress_stream(
            follow_list,
            self._after_received
        )

        return None

    def _after_received(self, content: ReplyToActressContent) -> None:
        print(content)
        actress_id = get_dmm_id_by_twitter_id(
            twitter_id=content.user_id
        )

        if isinstance(
            items := self.dmm_repository.get_items(
                GetDmmItemsParams.create_get_items_by_actress_id_params(
                    actress_id=actress_id,
                    hits=20,
                )
            ),
            Failure
        ):
            items.print_failure()
            return None

        items = self._filter_items(items)

        if len(items) == 0:
            SlackClient().send_alert("actress_idをもとにitemが取得できませんでした.actress_idが間違っているかもしれません")
            return None

        item, message = self._get_item(items)
        print(item, message)

        # TODO: MQにリクエストはrepositoryを作成するべき
        self.session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGIN_NAME,
        )

        sqs_client = self.session.client("sqs")

        response = sqs_client.send_message(
            QueueUrl=AWS_QUEUE_URL,
            MessageBody=json.dumps(
                {
                    "tweet_id": content.tweet_id,
                    "screen_name": content.screen_name,
                    "item": asdict(item),
                    "message": message,
                },
                ensure_ascii=False,
            ),
            MessageGroupId="REPLY",
        )

    # actressは単体
    def _filter_items(self, items: List['Item']) -> List['Item']:
        return list(
            filter(
                lambda item: len(item.actresses) == 1,
                items,
            )
        )

    def _get_item(self, items: List['Item']) -> tuple['Item', str]:
        campaign_result: List[tuple['Item', str]] = []
        limited_time_sale_result: List[tuple['Item', str]] = []

        # TODO: tupleで返すのどうにかしたい。campaignは"”で返してるのびみょい
        for item in items:
            if item.campaign != []:
                campaign_result.append((item, ""))

            if list(
                filter(
                    lambda genre: genre.id == 6565,
                    item.genres
                )
            ) != []:
                limited_time_sale_result.append((item, "期間限定セール中"))

        if(len(campaign_result) > 0):
            return random.choice(campaign_result)
        elif(len(limited_time_sale_result) > 0):
            return random.choice(limited_time_sale_result)
        else:
            return (random.choice(items[:3]), "大人気作品")
