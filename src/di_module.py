from config import (
    AWS_ACCESS_KEY_ID, AWS_REGIN_NAME, AWS_SECRET_KEY, DYNAMO_DB_TABLE_NAME, WP_APP_PASS, WP_BASE_URL, WP_USER, TWITTER_ACCESS_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_CONSUMER_SECRET, TWITTER_CONSUMER_TOKEN, TWITTER_STREAM_FILTER_FOLLOW
)
from repository.dmm_repository import AbstractDmmRepository, DmmRepository
from repository.dynano_db_repository import AbstractDynamoDbRepository, DynamoDbRepository
from datasource.remote.dmm_api_client import DmmApiClient
from datasource.remote.dynamo_db_api_client import DynamoDbApiClient
from repository.twitter_repository import AbstractTwitterRepository, TwitterRepository
from repository.wordpress_repository import AbstractWordPressRepository, WordPressRepository
from datasource.remote.wordpress_api_client import WordPressApiClient
from datasource.remote.twitter_api_client import TwitterApiClient
from injector import Module, Binder
from datasource.remote.twitter_stream_client import TwitterStreamListener
from usecase.samurai_recommend_usecase import SamuraiRecommendInteractor, SamuraiRecommendUseCase
from usecase.reservation_usecase import ReservationInteractor, ReservationUseCase
from presenter.reservation_presenter import AbstractReservationPresenter, ConsoleReservationPresenter
from presenter.release_presenter import AbstractReleasePresenter, ConsoleReleasePresenter
from usecase.release_usecase import ReleaseInteractor, ReleaseUseCase
from usecase.popular_usecase import PopularInteractor, PopularUseCase
from usecase.limited_time_sale_usecase import LimitedTimeSaleInteractor, LimitedTimeSaleUseCase
from usecase.same_reply_usecase import SameReplyInteractor, SameReplyUseCase
from datasource.remote.twitter_stream_client import TwitterStreamClient
from presenter.popular_presenter import AbstractPopularPresenter, ConsolePopularPresenter


class DIModule(Module):
    def configure(self, binder: Binder):
        binder.bind(AbstractDmmRepository, to=DmmRepository(DmmApiClient()))
        binder.bind(AbstractDynamoDbRepository, to=DynamoDbRepository(
            DynamoDbApiClient(
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_KEY,
                regin_name=AWS_REGIN_NAME,
                table_name=DYNAMO_DB_TABLE_NAME
            )
        ))
        binder.bind(AbstractWordPressRepository, to=WordPressRepository(
            WordPressApiClient(
                url=WP_BASE_URL,
                user=WP_USER,
                password=WP_APP_PASS
            )
        ))
        binder.bind(
            AbstractTwitterRepository,
            to=TwitterRepository(
                TwitterApiClient(
                    consumer_token=TWITTER_CONSUMER_TOKEN,
                    consumer_secret=TWITTER_CONSUMER_SECRET,
                    access_token=TWITTER_ACCESS_TOKEN,
                    access_secret=TWITTER_ACCESS_SECRET
                ),
                TwitterStreamClient(
                    consumer_token=TWITTER_CONSUMER_TOKEN,
                    consumer_secret=TWITTER_CONSUMER_SECRET,
                    access_token=TWITTER_ACCESS_TOKEN,
                    access_secret=TWITTER_ACCESS_SECRET,
                    stream_listener=TwitterStreamListener(),
                    stream_filter_follow=TWITTER_STREAM_FILTER_FOLLOW,
                )
            )
        )
        binder.bind(ReservationUseCase, to=ReservationInteractor)
        binder.bind(AbstractReservationPresenter,
                    to=ConsoleReservationPresenter)
        binder.bind(ReleaseUseCase, to=ReleaseInteractor)
        binder.bind(AbstractReleasePresenter, to=ConsoleReleasePresenter)
        binder.bind(PopularUseCase, to=PopularInteractor)
        binder.bind(AbstractPopularPresenter, to=ConsolePopularPresenter)
        binder.bind(LimitedTimeSaleUseCase, to=LimitedTimeSaleInteractor)
        binder.bind(SameReplyUseCase, to=SameReplyInteractor)
        binder.bind(SamuraiRecommendUseCase, to=SamuraiRecommendInteractor)
