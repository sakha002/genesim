from typing import TypeVar
from .service import Service
from .assetgroup import AssetGroup


ServiceT = TypeVar("ServiceT", bound="Service")

AssetGroupT = TypeVar("AssetGroupT", bound="AssetGroup")