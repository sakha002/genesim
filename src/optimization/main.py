from typing import List
from .data.input_parser import InputData
from .parameters.intervals import Interval
from .load import Load
from .solar import Solar
from .battery import Battery
from .site import Site
from .model import Model
from .asset import Asset
from .energy_import_charge import EnergyImportCharge
from .parameters.tariff_charges import EnergyImportChargeParameters
from .parameters.site import SiteParameters
from .parameters.solar import SolarParameters
from .parameters.battery import BatteryParameters
from .parameters.load import LoadParameters


INPUT_DATA_PATH = "data/input_data.csv"





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
        energy_import_charge=0.1,
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

    
    service1 = EnergyImportCharge(
        model=model,
        service_params=energy_import_charge_params,
    )
    
    asset_group1: Site = Site(
        model=model,
        assets=assets,
        services=[service1],
        asset_group_params=site_params,
    )
    
    # this part has to be done better later!
    for asset in assets:
        asset.add_service_constraints()
    
    model.solve(solver="CBC", verbose=True)
    
    
                









if __name__ == "__main__":
    main()