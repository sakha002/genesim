from abc import ABC
from typing import TypeVar

from optclient.solver_utils.isolver  import ISolver
from optclient.solver_utils.variable import Variable, VarType
from optclient.solver_utils.expression import LinExpr
from optclient.solver_utils.constraint import LinConstraint, ConstrSense

from src.genesym.elements.element import Element
from src.genesym.parameters.horizons.horizon import Interval
from src.genesym.parameters.scenarios.scenario import Scenario

from src.genesym.parameters.assets.asset_product_request import ParamAssetProductRequestT
from src.genesym.parameters.shared.asset_group_product_request import ParamAssetGroupProductRequestT



class AssetGroupProductRequestPeriod(Element, ABC):
    def __init__(
        self,
        model: ISolver,
        name: str,
        interval: Interval,
        scenario: Scenario,
        product_request_param: ParamAssetGroupProductRequestT,
    ):
        # this will be the product inerval or asset interval?
        # do we want to be able to branch out, for different products?
        # for assets, the needs of the products was supposed to be abstracted.
        super().__init__(model, name, interval, scenario)

        self.add_variable(
            name=f'asset_group_product_request_{self.name}_P_out',
            variable=Variable(
                name=f'asset_group_product_request_{self.name}_P_out',
                vtype=VarType.real,
                lower_bound=product_request_param.p_out_min,
                upper_bound=product_request_param.p_out_max
            )
        )
        self.add_variable(
            name=f'asset_group_product_request_{self.name}_E_out',
            variable=Variable(
                name=f'asset_group_product_request_{self.name}_E_out',
                vtype=VarType.real,
                lower_bound=product_request_param.e_out_min,
                upper_bound=product_request_param.e_out_max
            )
        )
        self.add_variable(
            name=f'asset_group_product_request_{self.name}_P_in',
            variable=Variable(
                name=f'asset_group_product_request_{self.name}_P_in',
                vtype=VarType.real,
                lower_bound=product_request_param.p_in_min,
                upper_bound=product_request_param.p_in_max
            )
        )
        self.add_variable(
            name=f'asset_group_product_request_{self.name}_E_in',
            variable=Variable(
                name=f'asset_group_product_request_{self.name}_E_in',
                vtype=VarType.real,
                lower_bound=product_request_param.p_in_min,
                upper_bound=product_request_param.p_in_max
            )
        )
        self.add_expression(
            name=f'asset_group_product_request_{self.name}_E_net',
            expression=LinExpr(
                name=f'asset_group_product_request_{self.name}_E_net',
                variables=[
                    self.variables[f'asset_group_product_request_{self.name}_E_out'],
                    self.variables[f'asset_group_product_request_{self.name}_E_in'],
                ],
                coefs=[1.0, -1.0],
                const=0.0,
            )
        )
        self.add_variable(
            name=f'asset_group_product_request_{self.name}_P_net',
            variable=Variable(
                name=f'asset_group_product_request_{self.name}_P_net',
                vtype=VarType.real,
                lower_bound= max(product_request_param.p_in_min, product_request_param.p_out_min),
                upper_bound= max(product_request_param.p_out_max, product_request_param.p_in_max),
            )
        )
        self.add_constraint(
            name=f'asset_group_product_request_{self.name}_P_net_P_in',
            constraint=LinConstraint(
                name=f'asset_group_product_request_{self.name}_P_net_P_in',
                expr=LinExpr(
                    name=f'asset_group_product_request_{self.name}_P_net_P_in',
                    variables=[
                        self.variables[f'asset_group_product_request_{self.name}_P_net'],
                        self.variables[f'asset_group_product_request_{self.name}_P_in'],
                    ],
                    coefs=[1.0, -1.0],
                    const=0.0,
                ),
                rhs=0.0,
                sense=ConstrSense.geq,
            )
        )
        self.add_constraint(
            name=f'asset_group_product_request_{self.name}_P_net_P_out',
            constraint=LinConstraint(
                name=f'asset_group_product_request_{self.name}_P_net_P_out',
                expr=LinExpr(
                    name=f'asset_group_product_request_{self.name}_P_net_P_out',
                    variables=[
                        self.variables[f'asset_group_product_request_{self.name}_P_net'],
                        self.variables[f'asset_group_product_request_{self.name}_P_out'],
                    ],
                    coefs=[1.0, -1.0],
                    const=0.0,
                ),
                rhs=0.0,
                sense=ConstrSense.geq,
            )
        )




#
# That is a big problem there, At least I don't quite remember
# we define a name for variable, and for add_var function,
# we add it to the model and to the Element, what are the names in
# model and in the elment?

# here we need to Specially pay attention that in each interval 
# both P_in and P_out may take positive values
# so in a sense P is still defined as net Power
# in that interval we could go by P=P_out - P_in
# but the meaning of P would be unclear
# if we say that P is the maximum power in any direction
# then we could model P>Pin, P>P_out



# when I work on the higher layer of code, and notice a problem
# shortcomming in lower layers, what should I do
# example case here is the name defenition of variables
# some assumptions made don't quite work
# and I don't want to just leave my current line of thought