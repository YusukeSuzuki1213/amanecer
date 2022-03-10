from di_module import DIModule
from controller import Controller
from injector import Injector
from log import SlackClient
import traceback


if __name__ == "__main__":
    injector = Injector([DIModule])
    controller = injector.get(Controller)

    try:
        controller.reply_to_actress()
    except Exception as e:
        print(traceback.format_exc())
        print(e)
        SlackClient().send_alert(traceback.format_exc())
        SlackClient().send_alert(e)
