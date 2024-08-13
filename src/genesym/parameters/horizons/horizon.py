from typing import List
from dataclasses import  dataclass
from datetime import datetime


@dataclass
class Interval:
    index: int
    interval_start: datetime
    interval_end: datetime

@dataclass
class Horizon:
    intervals: List[Interval]