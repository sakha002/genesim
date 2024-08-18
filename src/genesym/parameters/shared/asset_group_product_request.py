from dataclasses import dataclass
from typing import TypeVar, Optional

from src.genesym.parameters.types import ProductType

ProductTypeT = TypeVar("ProductTypeT", bound=ProductType)

@dataclass
class AssetGroupProductRequest:
    asset_group_name = str
    product_type: ProductTypeT
    p_out_max: Optional[float] = None
    p_in_max: Optional[float] = None
    p_out_min: float = 0.0
    p_in_min: float = 0.0
    e_out_max: Optional[float] = None
    e_in_max: Optional[float] = None
    e_out_min: float = 0.0
    e_in_min: float = 0.0
    throughput: Optional[float] = None
    call_chance: Optional[float] = None

ParamAssetGroupProductRequestT = TypeVar('ParamAssetGroupProductRequestT', bound=AssetGroupProductRequest)
