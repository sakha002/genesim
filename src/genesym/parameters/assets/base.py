from dataclasses import dataclass
from abc import ABC
from typing import Dict, TypeVar

from src.genesym.parameters.assets.asset_period import AssetPeriod


AssetPeriodT = TypeVar("AssetPeriodT", bound=AssetPeriod)

@dataclass
class AssetParam(ABC):
    asset_periods: Dict[int, Dict[int, AssetPeriodT]]