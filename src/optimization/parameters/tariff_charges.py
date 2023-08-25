
from .service import ServiceParameters
from .intervals import Interval
from typing import List
from datetime import datetime
from dataclasses import dataclass

@dataclass
class EnergyImportChargeParameters(ServiceParameters):
    import_charge_rate: float

    
    @staticmethod
    def create_energy_import_charges(
        intervals: List[Interval],
        import_charge_rate: float,
    ):
        return EnergyImportChargeParameters(
            name="energy_import_charges",
            intervals=intervals,
            P_in_max=[None for _ in intervals],
            P_out_max=[None for _ in intervals],
            P_in_min=[0 for _ in intervals],
            P_out_min=[0 for _ in intervals],
            import_charge_rate=import_charge_rate,
        )
        
    
    
@dataclass
class EnergyExportChargeParameters(ServiceParameters):
    export_charge_rate: float
    
    @staticmethod
    def create_energy_export_charges(
        intervals: List[Interval],
        export_charge_rate: float,
    ):
        return EnergyExportChargeParameters(
            name="energy_export_charges",
            intervals=intervals,
            export_charge_rate=export_charge_rate,
            P_in_max=[None for _ in intervals],
            P_out_max=[None for _ in intervals],
            P_in_min=[0 for _ in intervals],
            P_out_min=[0 for _ in intervals],
        )

@dataclass
class DemandResponseChargeParameters(ServiceParameters):
    demand_respond_charge_rate: float
    demand_response_period_start: datetime
    demand_response_period_end: datetime
    
    @staticmethod
    def create_demand_respond_charges(
        intervals: List[Interval],
        demand_respond_charge_rate: float,
        demand_response_period_start: datetime,
        demand_response_period_end: datetime,
    ) -> "DemandResponseChargeParameters":
        return DemandResponseChargeParameters(
            name="demand_response_charges",
            intervals=intervals,
            demand_respond_charge_rate=demand_respond_charge_rate,
            demand_response_period_start=demand_response_period_start,
            demand_response_period_end=demand_response_period_end,
            P_in_max=[None for _ in intervals],
            P_out_max=[None for _ in intervals],
            P_in_min=[0 for _ in intervals],
            P_out_min=[0 for _ in intervals],
        )
    
@dataclass
class DemandChargeParameters(ServiceParameters):
    demand_charge_rate: float
    demand_charge_period_start: datetime
    demand_charge_period_end: datetime
    
    
    @staticmethod
    def create_demand_charges(
        intervals: List[Interval],
        demand_charge_rate: float,
        demand_charge_period_start: datetime,
        demand_charge_period_end: datetime,
    ) -> "DemandChargeParameters":
        return DemandChargeParameters(
            name="demand_charges",
            intervals=intervals,
            demand_charge_rate=demand_charge_rate,
            demand_charge_period_start=demand_charge_period_start,
            demand_charge_period_end=demand_charge_period_end,
            P_in_max=[None for _ in intervals],
            P_out_max=[None for _ in intervals],
            P_in_min=[0 for _ in intervals],
            P_out_min=[0 for _ in intervals],
        )
    
    