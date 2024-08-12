from abc import ABC

from typing import TypeVar, Generic
# from src.genesym.elements.element_group import ElementGroup

from src.genesym.parameters.assets.base import AssetParams
from src.genesym.parameters.model import ModelParams



AssetParamsT = TypeVar('AssetParamsT', bound=AssetParams)
ModelParamsT = TypeVar('ModelParamsT', bound=ModelParams)


class Asset(ABC):

    def __init__(
        asset_params: AssetParams,
        model_params: ModelParams,

    ):
        






# so we could define an Asset as Generic class that is configurable.
# but knowing that an Asset will not ever be instantiated, do we still need to use generic type hinting
# also in the other model, we used variables as an atribute/argument that was passed
# now if we define Asset as an element group should we pass elements as args
# or what part of the model would be created at the asset level configurable?