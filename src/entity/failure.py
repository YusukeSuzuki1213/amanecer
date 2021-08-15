from dataclasses import dataclass
from typing import Union


@dataclass
class Failure:
    message: str
    traceback: Union[str, None] = None

    def print_failure(self):
        print('Message: {}'.format(self.message))
        print('Traceback: {}'.format(self.traceback))
