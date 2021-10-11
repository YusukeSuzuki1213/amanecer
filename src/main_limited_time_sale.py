from di_module import DIModule
from controller import Controller
from injector import Injector


if __name__ == "__main__":
    injector = Injector([DIModule])
    controller = injector.get(Controller)

    controller.tweet_limited_time_sale_item()
