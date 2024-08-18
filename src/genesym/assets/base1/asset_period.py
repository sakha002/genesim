from abc import ABC
from typing import TypeVar

from optclient.solver_utils.isolver  import ISolver
from optclient.solver_utils.variable import Variable, VarType
from optclient.solver_utils.expression import LinExpr

from src.genesym.elements.element import Element
from src.genesym.parameters.assets.asset_period import AssetPeriod as AssetPeriodParam

from src.genesym.parameters.horizons.horizon import Interval
from src.genesym.parameters.scenarios.scenario import Scenario


class AssetPeriod(Element, ABC):
    def __init__(
        self,
        model: ISolver,
        name: str,
        interval: Interval,
        scenario: Scenario,
        asset_period_param: AssetPeriodParam,
    ):
        super().__init__(model, name, interval, scenario)
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

AssetPeriodT = TypeVar("AssetPeriodT", bound=AssetPeriod)
