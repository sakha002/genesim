from dataclasses import dataclass
from abc import ABC
from typing import Dict, TypeVar

from src.genesym.parameters.assets.asset_period import ParamAssetPeriodT
from src.genesym.parameters.assets.asset_product_request import ParamAssetProductRequestT
from src.genesym.parameters.types import ScenarioIndex, IntervIndex, ProductTypeT


@dataclass
class ParamAsset(ABC):
    asset_name: str
    asset_id: int
    asset_periods: Dict[ScenarioIndex, Dict[IntervIndex, ParamAssetPeriodT]]
    asset_product_requests: Dict[
        ScenarioIndex,
        Dict[
            IntervIndex, 
            Dict[ProductTypeT, ParamAssetProductRequestT],
        ],                            
    ]


ParamAssetT = TypeVar('ParamAssetT', bound=ParamAsset)
