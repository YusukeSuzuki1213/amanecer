from output_data.popular_output_data import PopularOutputData
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
from input_data.popular_input_data import PopularInputData
from presenter.popular_presenter import AbstractPopularPresenter


class PopularUseCase(metaclass=ABCMeta):
    @inject
    def __init__(self, dmm_repository: AbstractDmmRepository, dynamo_db_repository: AbstractDynamoDbRepository, wordpress_repository: AbstractWordPressRepository, twitter_repository: AbstractTwitterRepository, presenter: AbstractPopularPresenter):
        self.dmm_repository = dmm_repository
        self.dynamo_db_repository = dynamo_db_repository
        self.wordpress_repository = wordpress_repository
        self.twitter_repository = twitter_repository
        self.presenter = presenter

    @abstractmethod
    def handle(self, input_data: PopularInputData) -> None:
        pass


class PopularInteractor(PopularUseCase):
    def handle(self, input_data: PopularInputData) -> None:

        # DMM APIから商品取得
        if isinstance(items := self.dmm_repository.get_items(
            GetDmmItemsParams.create_get_popular_item_params()
        ), Failure):
            return self.presenter.output_error(items)

        # 取得した商品をDBに登録(DBにまだ保存されていないものだけ)
        if isinstance(stored_item_ids := self.dynamo_db_repository.add_all(
            DynamoDbAddAllParams.create_dynamo_db_add_all_params_list(
                items=items,
                datetime_now=input_data.datetime_now
            )
        ), Failure):
            return self.presenter.output_error(stored_item_ids)

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

        # 人気アイテムを取得 from DynamoDB
        if isinstance(popular_item := self.dynamo_db_repository.get_popular_item(), Failure):
            return self.presenter.output_error(popular_item)

        # DBに人気アイテムがなかったら
        if popular_item is None:
            return self.presenter.output(PopularOutputData(
                items,
                stored_items,
                None,
                None
            ))

        # ツイート
        if isinstance(tweet_id := self.twitter_repository.tweet(
            TweetParams.create_popular_tweet_params(popular_item)
        ), Failure):
            return self.presenter.output_error(tweet_id)

        # ツイートのIDをDBに保存
        if isinstance(result_update_tweet_id := self.dynamo_db_repository.update_tweet_id_as_popular(
            DynamoDbUpdateTweetIdParams.create_update_tweet_id_params(
                popular_item, tweet_id)
        ), Failure):
            return self.presenter.output_error(result_update_tweet_id)

        return self.presenter.output(
            PopularOutputData(
                items,
                stored_items,
                popular_item,
                tweet_id
            )
        )
