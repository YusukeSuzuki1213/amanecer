from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReleaseInputData:
    datetime_now: datetime
