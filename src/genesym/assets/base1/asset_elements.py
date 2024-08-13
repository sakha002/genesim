from typing import Dict, Callable, Optional, TypeVar
from src.genesym.elements.element_group import ElementGroup, Element

from abc import ABC
from src.genesym.assets.base1.contracts import AssetParamT, ModelParamT

from src.genesym.parameters.assets.asset_period import AssetPeriod as AssetPeriodParam
from src.genesym.parameters.assets.base import AssetParam

from src.genesym.parameters.horizons.horizon import Interval
from src.genesym.parameters.scenarios.scenario import Scenario
from optclient.solver_utils.isolver  import ISolver
from optclient.solver_utils.variable import Variable, VarType
from optclient.solver_utils.expression import LinExpr


AssetPeriodParamT = TypeVar("AssetPeriodParamT", bound=AssetPeriodParam)

class AssetPeriod(Element, ABC):
    def __init__(
        self,
        asset_period_param: AssetPeriodParam,
        model: ISolver,
        interval: Interval,
        scenario: Scenario,
        name: str,
    ):
        super().__init__()
        self.model = model
        self.interval = interval
        self.scenario = scenario
        self.name = name

        self.add_variable(
            name='P_in',
            variable=Variable(
                name='P_in',
                vtype=VarType.real,
                lower_bound=asset_period_param.p_in_min,
                upper_bound=asset_period_param.p_in_max,
            )
        )
        self.add_variable(
            name='E_in',
            variable=Variable(
                name='E_in',
                vtype=VarType.real,
                lower_bound=asset_period_param.e_in_min,
                upper_bound=asset_period_param.e_in_max,
            )
        )
        self.add_variable(
            name='P_out',
            variable=Variable(
                name='P_out',
                vtype=VarType.real,
                lower_bound=asset_period_param.p_out_min,
                upper_bound=asset_period_param.p_out_max,
            )
        )
        self.add_variable(
            name='E_out',
            variable=Variable(
                name='E_out',
                vtype=VarType.real,
                lower_bound=asset_period_param.e_out_min,
                upper_bound=asset_period_param.e_out_max,
            )
        )

        self.add_expression(
            name="P_net",
            expression=LinExpr(
                name='P_net',
                variables=[self.variables['P_out'], self.variables['P_in']],
                coefs=[1.0, -1.0],
                const=0.0,
            ),
        )
        self.add_expression(
            name="E_net",
            expression=LinExpr(
                name='E_net',
                variables=[self.variables['E_out'], self.variables['E_in']],
                coefs=[1.0, -1.0],
                const=0.0,
            ),
        )

class AssetElementG(ElementGroup):
    def __init__(
        self,
        model: ISolver,
        model_param: ModelParamT,
        asset_param: AssetParamT,

    ):
        super().__init__()
        self._initilize_asset_periods(
            model=model,
            model_param=model_param,
            asset_param=asset_param,
        )


 
    def _initilize_asset_periods(
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