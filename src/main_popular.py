from di_module import DIModule
from controller import Controller
from injector import Injector
from datetime import datetime

if __name__ == "__main__":
    injector = Injector([DIModule])
    controller = injector.get(Controller)

    controller.tweet_popular_items(
        datetime_now=datetime.now()
    )
