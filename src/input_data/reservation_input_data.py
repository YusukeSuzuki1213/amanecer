from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReservationInputData:
    datetime_now: datetime
