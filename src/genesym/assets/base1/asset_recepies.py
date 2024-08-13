from abc import ABC
from typing import Optional, Dict, Callable

from src.genesym.assets.base1.contracts import AssetParamsT, ModelParamsT
from src.genesym.assets.base1.asset_elements import AssetElementsT

AssetRecepieInputT = Callable[[AssetParamsT, ModelParamsT, AssetElementsT], None]

class AssetRecepies(ABC):
    objective_methods: Optional[Dict[str, AssetRecepieInputT]]
    constraint_methods: Optional[Dict[str, AssetRecepieInputT]]



# this class will hold a collection of methods that take in parameters and some ElementGroup
# as input, and modify elements and "the model" by adding constraints, objectives, expressions, etc.
# or maybe even variables,