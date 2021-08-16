from entity.params.dynamo_db_get_items_params import DynamoDbGetItemsForSpecificReleaseDateParams
from output_data.release_output_data import ReleaseOutputData
from presenter.release_presenter import AbstractReleasePresenter
from input_data.release_input_data import ReleaseInputData
from output_data.release_output_data import ReleaseOutputData
from entity.params.dynamo_db_update_tweet_id_params import DynamoDbUpdateTweetIdParams
from entity.params.twitter_tweet_params import TweetParams
from entity.params.dynamo_db_update_article_url_params import DynamoDbUpdateArticleUrlParams
from entity.params.wordpress_post_article_params import PostArticleToWpParams
from entity.params.wordpress_upload_media_params import UploadMediaToWpParams
from entity.params.dynamo_db_add_all_params import DynamoDbAddAllParams
from entity.failure import Failure
from entity.params.get_dmm_items_params import GetDmmItemsParams
from repository.twitter_repository import AbstractTwitterRepository
from repository.wordpress_repository import AbstractWordPressRepository
from repository.dynano_db_repository import AbstractDynamoDbRepository
from repository.dmm_repository import AbstractDmmRepository
from injector import inject
from abc import ABCMeta, abstractmethod
from typing import cast, List
import json
from dataclasses import asdict


class ReleaseUseCase(metaclass=ABCMeta):
    @inject
    def __init__(self, dmm_repository: AbstractDmmRepository, dynamo_db_repository: AbstractDynamoDbRepository, wordpress_repository: AbstractWordPressRepository, twitter_repository: AbstractTwitterRepository, presenter: AbstractReleasePresenter):
        self.dmm_repository = dmm_repository
        self.dynamo_db_repository = dynamo_db_repository
        self.wordpress_repository = wordpress_repository
        self.twitter_repository = twitter_repository
        self.presenter = presenter

    @abstractmethod
    def handle(self, input_data: ReleaseInputData) -> None:
        pass


class ReleaseInteractor(ReleaseUseCase):
    def handle(self, input_data: ReleaseInputData) -> None:
        posted_data: List[ReleaseOutputData.PostedData] = []

        # DMM APIから商品取得
        if isinstance(items := self.dmm_repository.get_items(
            GetDmmItemsParams.create_get_release_item_params(
                input_data.datetime_now
            )
        ), Failure):
            self.presenter.output_error(items)
            return None

        # 取得した商品をDBに登録(DBにまだ保存されていないものだけ)
        if isinstance(stored_item_ids := self.dynamo_db_repository.add_all(
            DynamoDbAddAllParams.create_dynamo_db_add_all_params_list(
                items=items,
                datetime_now=input_data.datetime_now
            )
        ), Failure):
            self.presenter.output_error(stored_item_ids)
            return None

        # DBに保存できたcontent_idから、Itemを取得
        stored_items = list(
            filter(
                lambda item: item.content_id in cast(
                    List[str], stored_item_ids),
                items
            )
        )

        for item in stored_items:
            # WordPressにサムネ写真をアップロード
            if isinstance(media_id := self.wordpress_repository.upload_media(
                UploadMediaToWpParams.create_upload_media_params(
                    item.content_id,
                    item.image_url
                )
            ), Failure):
                self.presenter.output_error(media_id)
                continue

            # WordPressに記事を投稿
            if isinstance(article_url := self.wordpress_repository.post(
                PostArticleToWpParams.create_post_article_params(
                    item,
                    media_id
                )
            ), Failure):
                self.presenter.output_error(article_url)
                continue

            # DBに記事のURLを追加
            if isinstance(result_article_url := self.dynamo_db_repository.update_article_url(
                DynamoDbUpdateArticleUrlParams.create_update_article_url_params(
                    item,
                    article_url
                )
            ), Failure):
                self.presenter.output_error(result_article_url)
                continue

        # 本日配信開始アイテムを取得 from DynamoDB
        if isinstance(items_released_today := self.dynamo_db_repository.get_items_for_specific_release_date(
            DynamoDbGetItemsForSpecificReleaseDateParams.create_get_items_params(
                input_data.datetime_now
            )
        ), Failure):
            self.presenter.output_error(items_released_today)
            return None

        for item in items_released_today:
            # ツイート
            if isinstance(tweet_id := self.twitter_repository.tweet(
                TweetParams.create_release_tweet_params(item)
            ), Failure):
                self.presenter.output_error(tweet_id)
                continue

            # ツイートのIDをDBに保存
            if isinstance(result_update_tweet_id := self.dynamo_db_repository.update_tweet_id_as_release(
                DynamoDbUpdateTweetIdParams.create_update_tweet_id_params(
                    item, tweet_id)
            ), Failure):
                self.presenter.output_error(result_update_tweet_id)
                continue

            posted_data.append(
                ReleaseOutputData.PostedData(
                    item,
                    tweet_id
                )
            )

        return self.presenter.output(
            ReleaseOutputData(
                items_from_dmm_api=items,
                items_stored_dynamo_db=stored_items,
                items_from_dynamo_db=items_released_today,
                posted_data=posted_data
            )
        )
