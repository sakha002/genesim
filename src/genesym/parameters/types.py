from enum import Enum, auto
from typing import NewType,TypeVar

ScenarioIndex = NewType("ScenarioIndex", int)
IntervIndex = NewType("IntervIndex", int)

AssetGroupName = NewType('AssetGroupName', str)

class ProductType(Enum):
    ENERGY = auto()
    REGUP = auto()
    REGDOWN = auto()

ProductTypeT = TypeVar('ProductTypeT', bound=ProductType)
