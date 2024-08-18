
from dataclasses import dataclass, field



@dataclass
class Scenario:
    index: int
    probabiliy: float
    name: str = field(default='')