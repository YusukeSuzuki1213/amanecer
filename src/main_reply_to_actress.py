import atexit
from di_module import DIModule
from controller import Controller
from injector import Injector
from log import SlackClient


def alert():
    SlackClient().send_alert("main_actress_reply.pyのプログラムが停止しました")


if __name__ == "__main__":
    atexit.register(alert)
    injector = Injector([DIModule])
    controller = injector.get(Controller)

    controller.reply_to_actress()
