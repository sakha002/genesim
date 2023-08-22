from .asset import Asset
from .model import Model, VarType
from .parameters.battery import BatteryParameters



class Battery(Asset):
    def __init__(
        self,
        model: Model,
        asset_params: BatteryParameters,
    ):
        
        super().__init__(
            model=model,
            asset_params=asset_params,
        )
        
        
        
        
        
        # self.add_battery_power_balance_constraints()
        # self.add_battery_energy_power_bind_constraints()
        
        return
    
    
    def add_battery_soc_vars(self) -> None:
        for interval in self.asset_params.intervals:
            self.model.add_var(
                name=f"battery_{self.name}_soc_t{interval.index}",
                var_type=VarType.REAL,
                lb=self.asset_params.min_soc,
                ub=self.asset_params.energy_capacity,
            )
        return
    
    
    def set_battery_soc_dynamic_constraints(self) -> None:
        
        for interval in self.asset_params.intervals:
            if interval.index == 0:
                self.model.add_constraint(
                    name=f"battery_{self.name}_soc_t{interval.index}_dynamic",
                    constraint=(
                        self.model.get_var(f"battery_{self.name}_soc_t{interval.index}")
                        ==  self.asset_params.initial_energy
                    ),
                )
            
            else:
                self.model.add_constraint(
                    name=f"battery_{self.name}_soc_t{interval.index}_dynamic",
                    constraint=(
                        self.model.get_var(f"battery_{self.name}_soc_t{interval.index}")
                        ==  self.model.get_var(f"battery_{self.name}_soc_t{interval.index - 1}")
                        + (self.model.get_var(f"asset_{self.name}_E_in_t{interval.index}") * self.asset_params.charge_efficiency)
                        - (self.model.get_var(f"asset_{self.name}_E_out_t{interval.index}") * (1 / self.asset_params.discharge_efficiency))
                    ),
                )

        
    