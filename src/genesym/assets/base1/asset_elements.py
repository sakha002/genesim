from typing import Dict, Callable, Optional, TypeVar
from src.genesym.elements.element_group import ElementGroup

from abc import ABC

from src.genesym.parameters.assets.asset_period import AssetPeriod as AssetPeriodParam
from src.genesym.assets.base1.asset_period import AssetPeriod
from optclient.solver_utils.isolver  import ISolver

from src.genesym.parameters.assets.asset import ParamAssetT
from src.genesym.parameters.model import ParamModelT

AssetPeriodParamT = TypeVar("AssetPeriodParamT", bound=AssetPeriodParam)

class AssetElementG(ABC, ElementGroup):
    def __init__(
        self,
        model: ISolver,
        model_param: ParamModelT,
        asset_param: ParamAssetT,
    ):
        # here we are adding AssetPeriods as elements to the 
        # AssetElements, but I don't like it that we cannot see
        # AssetPeriods as Attribute of the AssetElement
        # At the Same time If We are to Access the "Elements"
        # of the Asset Within self.elements, then
        super().__init__()
        self._initialize_asset_periods(
            model=model,
            model_param=model_param,
            asset_param=asset_param,
        )
        self._initialize_asset_product_requests(
            model=model,
            model_param=model_param,
            asset_param=asset_param,
        )

 
    def _initialize_asset_periods(
        self,
        model: ISolver,
        model_param: ModelParamT,
        asset_param: AssetParamT,
    ) -> None:
        
        for scenario in model_param.scenario_info.scenarios:
            for interval in model_param.horizon.intervals:
                self.add_element(
                    scenario=scenario.index,
                    interval=interval.index,
                    element=AssetPeriod(
                        model=model,
                        interval=interval,
                        scenario=scenario,
                        name='asset_period',
                        asset_period_params=asset_param.asset_periods[scenario.index][interval.index]
                    )
                )
        
    def _initialize_asset_product_requests(
        self,
        model: ISolver,
        model_param: ParamModelT,
        asset_param: ParamAssetT,
    ) -> None:
        pass 
        # for scenario in model_param.scenario_info.scenarios:
        #     for interval in model_param.horizon.intervals:
                # self.add_shared_element(
                #     scenario=scenario.index,
                #     interval=interval.index,
                #     element=
                # )
            

AssetElementGT = TypeVar('AssetElementGT', bound=AssetElementG)



# so here each objective method, we want it to be 
#
# let me recap what I came up before,
# An asset would make something be applied on AssetElements
# AssetOptProblem
# in legacy we have:
# Asset, AssetVariables, AssetOptProblem
# the other question, 
# We Need the Elements to ADD Objective/Constraints  to the Model
# So the Elements would need to be called by Recepies and then create, objectives, constraints, etc.
# we would need them to have AssetParams(ElementParams??), ProblemParams, and AssetElements(all of it? or Maybe Just an ElementGroup)

# do we need to have the asset (basic) variables, exprs, etc, already initiated, when they are called by the recepie?
# they were needed to be added to the model, when they were created, the Elements Vars, not elements itself.
#what are the asset Elements, and what we initializing AssetElements WIth