import os
from dotenv import load_dotenv

DYNAMO_DB_TABLE_NAME = 'items-3006'
DMM_GET_ITEMS_URL = 'https://api.dmm.com/affiliate/v3/ItemList'
AWS_REGIN_NAME = 'us-east-2'
WP_RESOURCE_NAME_POST = '/wp-json/wp/v2/posts'
WP_RESOURCE_NAME_MEDIA = '/wp-json/wp/v2/media'
WP_COTEGORY_ID = 1

load_dotenv()

# Twitter
TWITTER_CONSUMER_TOKEN = os.getenv('TWITTER_CONSUMER_TOKEN', '')
TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET', '')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN', '')
TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET', '')
TWITTER_SAMURAI_HASH_TAG = os.getenv('TWITTER_SAMURAI_HASH_TAG', '')

TWITTER_STREAM_FILTER_FOLLOW = (
    os.getenv('TWITTER_STREAM_FILTER_FOLLOW', '')).split(',')

if not TWITTER_CONSUMER_TOKEN:
    print('Specify TWITTER_CONSUMER_TOKEN as environment variable.')
    os.sys.exit(1)

if not TWITTER_CONSUMER_SECRET:
    print('Specify TWITTER_CONSUMER_SECRET as environment variable.')
    os.sys.exit(1)

if not TWITTER_ACCESS_TOKEN:
    print('Specify TWITTER_ACCESS_TOKEN as environment variable.')
    os.sys.exit(1)

if not TWITTER_ACCESS_SECRET:
    print('Specify TWITTER_ACCESS_SECRET as environment variable.')
    os.sys.exit(1)

# TODO: .envに定義されているかのチェック and '123,232'の形式になっているかのチェックを実装
if not TWITTER_STREAM_FILTER_FOLLOW:
    print('Specify TWITTER_STREAM_FILTER_FOLLOW as environment variable.')
    os.sys.exit(1)

if not TWITTER_SAMURAI_HASH_TAG:
    print('Specify TWITTER_SAMURAI_HASH_TAG as environment variable.')
    os.sys.exit(1)

# DMM
DMM_API_KEY = os.getenv('DMM_API_KEY', '')
DMM_AFFILIATE_ID = os.getenv('DMM_AFFILIATE_ID', '')

if not DMM_API_KEY:
    print('Specify DMM_API_KEY as environment variable.')
    os.sys.exit(1)

if not DMM_AFFILIATE_ID:
    print('Specify DMM_AFFILIATE_ID as environment variable.')
    os.sys.exit(1)

# AWS
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY', '')

if not AWS_ACCESS_KEY_ID:
    print('Specify AWS_ACCESS_KEY_ID as environment variable.')
    os.sys.exit(1)

if not AWS_SECRET_KEY:
    print('Specify AWS_SECRET_KEY as environment variable.')
    os.sys.exit(1)

# WordPress
WP_USER = os.getenv('WP_USER', '')
WP_APP_PASS = os.getenv('WP_APP_PASS', '')
WP_BASE_URL = os.getenv('WP_BASE_URL', '')

if not WP_USER:
    print('Specify WP_USER as environment variable.')
    os.sys.exit(1)

if not WP_APP_PASS:
    print('Specify WP_APP_PASS as environment variable.')
    os.sys.exit(1)

if not WP_BASE_URL:
    print('Specify WP_BASE_URL as environment variable.')
    os.sys.exit(1)

# DMM CRAWLER
DMM_CRAWLER_VIDEO_SERCH_URL = os.getenv('DMM_CRAWLER_VIDEO_SERCH_URL', '')
DMM_CRAWLER_URL = os.getenv('DMM_CRAWLER_URL', '')
DMM_CRAWLER_VIDEO_URL = os.getenv('DMM_CRAWLER_VIDEO_URL', '')

if not DMM_CRAWLER_VIDEO_SERCH_URL:
    print('Specify DMM_CRAWLER_VIDEO_SERCH_URL as environment variable.')
    os.sys.exit(1)

if not DMM_CRAWLER_URL:
    print('Specify DMM_CRAWLER_URL as environment variable.')
    os.sys.exit(1)

if not DMM_CRAWLER_VIDEO_URL:
    print('Specify DMM_CRAWLER_VIDEO_URL as environment variable.')
    os.sys.exit(1)

# SLACK
SLACK_API_TOKEN = os.getenv('SLACK_API_TOKEN', '')
SLACK_CHANNEL_NAME_FOR_SEND_LOG = os.getenv(
    'SLACK_CHANNEL_NAME_FOR_SEND_LOG', ''
)
if not SLACK_API_TOKEN:
    print('Specify SLACK_API_TOKEN as environment variable.')
    os.sys.exit(1)

if not SLACK_CHANNEL_NAME_FOR_SEND_LOG:
    print('Specify SLACK_CHANNEL_NAME_FOR_SEND_LOG as environment variable.')
    os.sys.exit(1)
