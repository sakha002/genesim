from __future__ import annotations
from service import Service
from model import Model
from parameters.tariff_charges import EnergyImportChargeParameters
# from opt_types import AssetGroupT

class EnergyImportCharge(Service):
    def __init__(
        self,
        model: Model,
        service_params: EnergyImportChargeParameters,
    ):
        super().__init__(
            model=model,
            service_params=service_params,
        )
        
        self.add_objective_terms()
        
        self.add_energy_power_bind_constraints()
        
        return
    
    
    
    def add_asset_group_coupling(self, asset_group: "assetgroup.AssetGroup") -> None:
        return
    
    
    # def add_service_power_constraints(self, asset_group: AssetGroupT) -> None:
        
    #     for interval in self.service_params.intervals:
    #         if self.model.get_var(f"service_{self.name}_P_in_t{interval.index}") is not None:
    #             self.model.add_constraint(
    #                 name=f"service_{self.name}_P_in_t{interval.index}_asset_requirements",
    #                 constraint=(
    #                     self.model.get_var(f"service_{self.name}_P_in_t{interval.index}")
    #                     ==  self.model.sum_vars(
    #                         vars=[
    #                             self.model.get_var(f"asset_{asset.name}_P_in_t{interval.index}")
    #                             for asset in asset_group.assets
    #                         ],
    #                     )
    #                     # self.model.get_var(f"asset_group_{asset.name}_P_in_t{interval.index}")
                        
                           
    #                 ),
    #             )
        

    def add_energy_power_bind_constraints(self) -> None:
        for interval in self.service_params.intervals:
            if self.model.get_var(f"service_{self.name}_P_in_t{interval.index}") is not None:
                self.model.add_constraint(
                    name=f"energy_import_charge_{self.name}_P_in_t{interval.index}_energy_bind",
                    constraint=(
                        self.model.get_var(f"service_{self.name}_P_in_t{interval.index}")
                        == self.model.get_var(f"service_{self.name}_E_in_t{interval.index}")
                    ),
                )
    
    def add_objective_terms(self) -> None:
        for interval in self.service_params.intervals:
            if self.model.get_var(f"service_{self.name}_P_in_t{interval.index}") is not None:
                self.model.add_objective_terms(
                    # name=f"service_{self.name}_P_in_t{interval.index}_cost",
                    objective_terms= (
                        self.model.get_var(f"service_{self.name}_P_in_t{interval.index}")
                        * self.service_params.import_charge_rate
                    )
                )
        return