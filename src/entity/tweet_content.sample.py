class TweetContent(object):

    @classmethod
    def get_reservation_tweet_content(cls) -> str:
        return '<予約商品のツイート内容>'

    @classmethod
    def get_release_tweet_content(cls) -> str:
        return '<配信開始商品のツイート内容>'

    @classmethod
    def get_popular_tweet_content(cls) -> str:
        return '<人気商品のツイート内容>'
