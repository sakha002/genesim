from dataclasses import dataclass
from typing import Dict, TypeVar

from src.genesym.parameters.shared.asset_group_product_request import ParamAssetGroupProductRequestT
from src.genesym.parameters.types import ProductTypeT, AssetGroupName


@dataclass
class AssetProductRequest:
    product_type: ProductTypeT
    asset_group_product_requests: Dict[
        AssetGroupName, ParamAssetGroupProductRequestT
    ]

ParamAssetProductRequestT = TypeVar("ParamAssetProductRequestT", bound=AssetProductRequest)
