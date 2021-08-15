from presenter.reservation_presenter import AbstractReservationPresenter, ConsoleReservationPresenter
from usecase.reservation_usecase import ReservationInteractor, ReservationUseCase
from injector import Module, Binder
from datasource.remote.twitter_api_client import TwitterApiClient
from datasource.remote.wordpress_api_client import WordPressApiClient
from repository.wordpress_repository import AbstractWordPressRepository, WordPressRepository
from repository.twitter_repository import AbstractTwitterRepository, TwitterRepository
from datasource.remote.dynamo_db_api_client import DynamoDbApiClient
from datasource.remote.dmm_api_client import DmmApiClient
from repository.dynano_db_repository import AbstractDynamoDbRepository, DynamoDbRepository
from repository.dmm_repository import AbstractDmmRepository, DmmRepository
from config import (
    AWS_ACCESS_KEY_ID, AWS_REGIN_NAME, AWS_SECRET_KEY, DYNAMO_DB_TABLE_NAME, WP_APP_PASS, WP_BASE_URL, WP_USER, TWITTER_ACCESS_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_CONSUMER_SECRET, TWITTER_CONSUMER_TOKEN
)


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
        binder.bind(AbstractTwitterRepository,
                    to=TwitterRepository(TwitterApiClient(
                        consumer_token=TWITTER_CONSUMER_TOKEN,
                        consumer_secret=TWITTER_CONSUMER_SECRET,
                        access_token=TWITTER_ACCESS_TOKEN,
                        access_secret=TWITTER_ACCESS_SECRET
                    )))
        binder.bind(ReservationUseCase, to=ReservationInteractor)
        binder.bind(AbstractReservationPresenter,
                    to=ConsoleReservationPresenter)
