
from dataclasses import dataclass, field
from typing import Optional



@dataclass
class Scenario:
    index: int
    probabiliy: float
    name: str = field(default='')