from typing import List
import cylp
from cvxpy import CBC
from datetime import time
from data.input_parser import InputData
from data.output_writer import OutputData
from parameters.intervals import Interval
from load import Load
from solar import Solar
from battery import Battery
from itc_site import ITCSite
from model import Model
from asset import Asset
from energy_import_charge import EnergyImportCharge
from energy_export_charge import EnergyExportCharge
from demand_import_charge import DemandImportCharge
from demand_response_charge import DemandResponseCharge
from parameters.tariff_charges import(
    EnergyImportChargeParameters,
    EnergyExportChargeParameters,
    DemandChargeParameters,
    DemandResponseChargeParameters,
)
from parameters.site import SiteParameters
from parameters.solar import SolarParameters
from parameters.battery import BatteryParameters
from parameters.load import LoadParameters

INPUT_DATA_PATH = "data/input_data.csv"
OUTPUT_DATA_PATH = "data/output_data.csv"




def main():
    
    inputs: List[InputData] = InputData.read_csv_file(INPUT_DATA_PATH)
    
    intervals: List[Interval] = Interval.create_intervals_from_input(
        time_stamps=[input_data.time_stamp for input_data in inputs]
    )
    
    load_params: LoadParameters = LoadParameters.read_load_data(
        intervals=intervals,
        load_vals=[input_data.load for input_data in inputs],
    )
    solar_params: SolarParameters = SolarParameters.read_solar_data(
        intervals=intervals,
        solar_vals=[input_data.solar for input_data in inputs],
    )
    battery_params: BatteryParameters = BatteryParameters.load_constant_battery_data(
        intervals=intervals,
        initial_energy=0,
        energy_capacity=53,
        charge_efficiency=0.95,
        discharge_efficiency=0.95,
        min_soc=0,
        nominal_power=25,
    )
    site_params: SiteParameters = SiteParameters.create_constant_limit_site(
        intervals=intervals,
        P_in_limit=1000,   # PCC limits We don't need this in this particular example, a large number so that it does not bind
        P_out_limit=1000,
    )
    energy_import_charge_params: EnergyImportChargeParameters = EnergyImportChargeParameters.create_energy_import_charges(
        intervals=intervals,
        import_charge_rate=0.1,
    )
    
    energy_export_charge_params: EnergyExportChargeParameters = EnergyExportChargeParameters.create_energy_export_charges(
        intervals=intervals,
        export_charge_rate=0.03,
    )
    
    demand_charge_params: DemandChargeParameters = DemandChargeParameters.create_demand_charges(
        intervals=intervals,
        demand_charge_rate=9,
        demand_charge_period_start=time(hour=17, minute=0),
        demand_charge_period_end=time(hour=21, minute=0),
    )
    
    demand_response_charge_params: DemandResponseChargeParameters = DemandResponseChargeParameters.create_demand_response_charges(
        intervals=intervals,
        demand_response_charge_rate=10,
        demand_response_period_start=time(hour=19, minute=0),
        demand_response_period_end=time(hour=20, minute=0),
    )
    
    
    model: Model = Model()
    
    asset1: Load = Load(
        model=model,
        asset_params=load_params,
    )
    asset2: Solar = Solar(
        model=model,
        asset_params=solar_params,
    )
    asset3: Battery = Battery(
        model=model,
        asset_params=battery_params,
    )
    assets: List[Asset]=[asset1, asset2, asset3]

    
    service1: EnergyImportCharge = EnergyImportCharge(
        model=model,
        service_params=energy_import_charge_params,
    )
    
    service2: EnergyExportCharge = EnergyExportCharge(
        model=model,
        service_params=energy_export_charge_params,
    )
    
    service3: DemandImportCharge = DemandImportCharge(
        model=model,
        service_params=demand_charge_params,
    )
    
    service4: DemandResponseCharge = DemandResponseCharge(
        model=model,
        service_params=demand_response_charge_params,
    )
    
    asset_group1: ITCSite = ITCSite(
        model=model,
        assets=assets,
        services=[service1, service2, service3, service4],
        asset_group_params=site_params,
    )
    
    
    model.solve(solver=CBC, verbose=True)
    
    
    battery_ac_powers: List[float] = asset3.get_battery_ac_power_vars()
    site_ac_powers: List[float] = asset_group1.get_site_ac_power_vars()
    
    
    outputs: List[OutputData] = [
        OutputData(
            time=interval.interval_end - interval.interval_duration,
            battery_ac_power=battery_ac_powers[interval.index],
            ppc_meter_ac_power=site_ac_powers[interval.index],
        ) for interval in intervals
    ]
    
    OutputData.write_to_csv(OUTPUT_DATA_PATH, outputs)
    
    var_vals = model.get_all_var_values()
    
    return
    
    
    
    
                









if __name__ == "__main__":
    main()