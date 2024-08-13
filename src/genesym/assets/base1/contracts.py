from typing import TypeVar

from src.genesym.parameters.assets.base import AssetParam
from src.genesym.parameters.model import ModelParam



AssetParamT = TypeVar('AssetParamT', bound=AssetParam)
ModelParamT = TypeVar('ModelParamT', bound=ModelParam)