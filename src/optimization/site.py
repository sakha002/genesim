from typing import List
from .assetgroup import AssetGroup
from .asset import Asset
from .model import Model, VarType
from .service import Service
from .parameters.site import SiteParameters



class Site(AssetGroup):
    
    def __init__(
        self,
        model: Model,
        assets: List[Asset],
        services: List[Service],
        asset_group_params: SiteParameters,
    ):
        super().__init__(
            model=model,
            assets=assets,
            services=services,
            asset_group_params=asset_group_params,
        )
        
        # self.add_site_soc_vars()
        # self.set_site_soc_dynamic_constraints()
        
        return
    
        