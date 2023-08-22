from typing import List
from .model import Model, VarType   
from .parameters.service import ServiceParameters

from .asset import Asset


class Service:
    def __init__(
        self,
        model: Model,
        service_params: ServiceParameters,
    ):
        
        self.name = service_params.name
        self.service_params = service_params
        self.model = model
        
        for interval in service_params.intervals:
            
            if service_params.P_out_max[interval.index] != 0:
                model.add_var(
                    name=f"service_{service_params.name}_P_out_t{interval.index}",
                    var_type=VarType.REAL,
                    lb=service_params.P_out_min,
                    ub=service_params.P_out_max,
                )
            
            if service_params.P_in_max[interval.index] != 0:
                model.add_var(
                    name=f"service_{service_params.name}_P_in_t{interval.index}",
                    var_type=VarType.REAL,
                    lb=service_params.P_in_min,
                    ub=service_params.P_in_max,
                )
                
            model.add_var(
                name=f"service_{service_params.name}_E_t{interval.index}",
                var_type=VarType.REAL,
            )
    


    def add_assets(self, assets: List[Asset]) -> None:
        
        for asset in assets:
            for interval in self.service_params.intervals:
                if (self.model.get_var(f"asset_{asset.name}_P_out_t{interval.index}") is not None) \
                    and (self.model.get_var(f"service_{self.name}_P_out_t{interval.index}") is not None):
                        self.model.add_var(
                            name=f"asset_{asset.name}_service_{self.name}_P_out_t{interval.index}_var",
                            var_type=VarType.REAL,
                            lb=0,
                            ub=self.service_params.P_out_max[interval.index],
                            # this could be bound to either asset or service power caps, or maybe both?
                        )
                
                if (self.model.get_var(f"asset_{asset.name}_P_in_t{interval.index}") is not None) \
                    and (self.model.get_var(f"service_{self.name}_P_in_t{interval.index}") is not None):
                        self.model.add_var(
                            name=f"asset_{asset.name}_service_{self.name}_P_in_t{interval.index}_var",
                            var_type=VarType.REAL,
                            lb=0,
                            ub=self.service_params.P_in_max[interval.index],
                        )
                
                self.model.add_var(
                    name=f"asset_{asset.name}_service_{self.name}_E_t{interval.index}_var",
                    var_type=VarType.REAL,
                )
        
        
        for interval in self.service_params.intervals:
            
            if self.model.get_var(f"service_{self.name}_P_out_t{interval.index}") is not None:
                self.model.add_constraint(
                    name=f"service_{self.name}_P_out_t{interval.index}_asset_bind",
                    constraint=(
                        self.model.get_var(f"service_{self.name}_P_out_t{interval.index}")
                        ==  self.model.sum_vars(
                            vars=[
                                self.model.get_var(f"asset_{asset.name}_service_{self.name}_P_out_t{interval.index}_var")
                                for asset in assets
                            ]
                        )
                    ),
                )
            
            if self.model.get_var(f"service_{self.name}_P_in_t{interval.index}") is not None:
                self.model.add_constraint(
                    name=f"service_{self.name}_P_in_t{interval.index}_asset_bind",
                    constraint=(
                        self.model.get_var(f"service_{self.name}_P_in_t{interval.index}")
                        == self.model.sum_vars(
                            vars=[
                                self.model.get_var(f"asset_{asset.name}_service_{self.name}_P_in_t{interval.index}_var")
                                for asset in assets
                            ]
                        )
                    ),
                )

            self.model.add_constraint(
                name=f"service_{self.name}_E_t{interval.index}_asset_bind",
                constraint=(
                    self.model.get_var(f"service_{self.name}_E_t{interval.index}")
                    == self.model.sum_vars(
                        vars=[
                            self.model.get_var(f"asset_{asset.name}_service_{self.name}_E_t{interval.index}_var")
                            for asset in assets
                        ]
                    )
                ),
            )
            
        return