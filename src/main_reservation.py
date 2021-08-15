from di_module import DIModule
from controller import Controller
from injector import Injector
from datetime import datetime

if __name__ == "__main__":
    injector = Injector([DIModule])
    controller = injector.get(Controller)

    controller.tweet_reservation_items(
        datetime_iso=datetime.now().replace(microsecond=0).isoformat()
    )
