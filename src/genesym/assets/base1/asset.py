from abc import ABC

from typing import TypeVar, Generic

from optclient.solver_utils.isolver import ISolver 

from src.genesym.assets.base1.asset_elements import AssetElementGT
from src.genesym.parameters.assets.asset import ParamAssetT
from src.genesym.parameters.model import ParamModelT




class Asset(ABC):

    def __init__(
        self,
        model: ISolver,
        asset_param: ParamAssetT,
        model_param: ParamModelT,
        asset_element_g: AssetElementGT,
    ):
        self.asset_model = asset_element_g(
            model=model,
            model_param=model_param,
            asset_param=asset_param,
        )
        






# so we could define an Asset as Generic class that is configurable.
# but knowing that an Asset will not ever be instantiated, do we still need to use generic type hinting
# also in the other model, we used variables as an atribute/argument that was passed
# now if we define Asset as an element group should we pass elements as args
# or what part of the model would be created at the asset level configurable?

# Do I need to (or prefered to) bring the AssetElements, Pre-populated, or populate
# as part of Asset Creation, Since The Key here is the Model, Model could be passed to AssetElements
# by The Asset