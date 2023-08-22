from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Optional


@dataclass
class Interval:
    interval_end: Optional[datetime]
    interval_duration: timedelta = timedelta(minutes=60)
    index: int
    