from typing import List
from .model import Model, VarType
from .asset import Asset
from .parameters.asset_group import AssetGroupParameters
from .service import Service

class AssetGroup:
    def __init__(
        self,
        model: Model,
        assets: List[Asset],
        services: List[Service],
        asset_group_params: AssetGroupParameters,
    ):
        self.name = asset_group_params.name
        self.model = model
        self.assets = assets
        self.services = services
        self.asset_group_params = asset_group_params

        for interval in asset_group_params.intervals:
            if asset_group_params.P_out_max[interval.index] != 0:
                model.add_var(
                    name=f"asset_group_{self.name}_P_out_t{interval.index}",
                    var_type=VarType.REAL,
                    lb=asset_group_params.P_out_min,
                    ub=asset_group_params.P_out_max,
                )
            
            if asset_group_params.P_in_max[interval.index] != 0:
                model.add_var(
                    name=f"asset_group_{self.name}_P_in_t{interval.index}",
                    var_type=VarType.REAL,
                    lb=asset_group_params.P_in_min,
                    ub=asset_group_params.P_in_max,
                )
                
            model.add_var(
                name=f"asset_group_{self.name}_E_t{interval.index}",
                var_type=VarType.REAL,
            )
            
            # we don't have this equality
            # model.add_constraint(
            #     name=f"asset_group_{name}_E_t{interval.index}_power_balance",
            #     constraint=(
            #         model.get_var(f"asset_group_{name}_E_t{interval.index}")
            #         ==  - model.get_var(f"asset_group_{name}_P_in_t{interval.index}")
            #         + model.get_var(f"asset_group_{name}_P_out_t{interval.index}")
            #     ),
            # )

        for interval in asset_group_params.intervals:
            if model.get_var(f"asset_group_{self.name}_P_out_t{interval.index}") is not None:
                model.add_constraint(
                    name=f"asset_group_{self.name}_P_out_t{interval.index}_asset_bind",
                    constraint=(
                        model.get_var(f"asset_group_{self.name}_P_out_t{interval.index}")
                        ==  model.sum_vars(
                            vars=[
                                model.get_var(f"asset_{asset.name}_P_out_t{interval.index}")
                                for asset in assets
                            ]
                        )
                    ),
                )
            
            if model.get_var(f"asset_group_{self.name}_P_in_t{interval.index}") is not None:
                model.add_constraint(
                    name=f"asset_group_{self.name}_P_in_t{interval.index}_asset_bind",
                    constraint=(
                        model.get_var(f"asset_group_{self.name}_P_in_t{interval.index}")
                        == model.sum_vars(
                            vars=[
                                model.get_var(f"asset_{asset.name}_P_in_t{interval.index}")
                                for asset in assets
                            ]
                        )
                    ),
                )
                
            model.add_constraint(
                name=f"asset_group_{self.name}_E_t{interval.index}_asset_bind",
                constraint=(
                    model.get_var(f"asset_group_{self.name}_E_t{interval.index}")
                    == model.sum_vars(
                        vars=[
                            model.get_var(f"asset_{asset.name}_E_t{interval.index}")
                            for asset in assets
                        ]
                    )
                ),
            )
               

        for service in services:
            service.add_assets(assets)
        
        for asset in assets:
            asset.add_services(services)
            
        
        
    
    
    # def add_services_power_requirement(self):
        
    #     for interval in self.asset_group_params.intervals:
    #         self.model.add_constraint(
    #             name=f"asset_group_{self.name}_P_out_t{interval.index}_service_requirement",
    #             constraint=(
    #                 self.model.get_var(f"asset_group_{self.name}_P_out_t{interval.index}")
    #                 == self.model.sum_vars(
    #                     vars=[
    #                         self.model.get_var(f"service_{service.name}_P_out_t{interval.index}")
    #                         for service in self.services
    #                     ]
    #                 )
    #             ),
    #         )
    
    
    # the relation of E_t and P_t will be determined under asset subclasses with respect to services?
