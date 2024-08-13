from typing import Optional
from dataclasses import dataclass, field

@dataclass
class Stage:
    index: int
    parent: Optional['Stage'] = None
    name: str = field(default='')