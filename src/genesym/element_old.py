from abc import ABC
from typing import Dict, List, Optional, Any

from optclient.solver_utils.isolver import ISolver
from optclient.solver_utils.variable import Variable
from optclient.solver_utils.expression import LinExpr
from optclient.solver_utils.constraint import LinConstraint

class Interval:
    index: int

class Scenario:
    index: int
    pass
    #unlike interval the meanng of a scenario can varry 
    # depending people's opinion
    # it relates to random variables to start!
    # sometimes a scenario is for a single parameter
    # often it is related to a number of parameters together
    # a scenario may involve 


# class ElementPeriod:
#     interval: Interval
#     model: ISolver   # should we add model all the way down?
#     # would perds want to add constrants, vars, expressions objectves
#     var_collect : Dict[str, Variable]
#     vars: List[Variable]
#     expressions: List[LinExpr]


class Parameter:
    intervals: List[Interval]
    scenarios: List[Scenario]

class AssetParam:
    pass

class AssetVar:
    power_vars: Dict[str, Variable]
    energy_vars: Dict[str, Variable]


class PeriodElement(ABC):
    model: ISolver
    variables: Dict[str, Variable]
    expressions: Dict[str, LinExpr]
    constraints: Dict[str, LinConstraint]
    objectives: Dict[str, LinExpr]
    interval: Optional[Interval]
    scenario: Optional[Scenario]
    name: str

    def __init__(self):
        self.variables = {}
        self.expressions = {}
        self.constraints = {}
        self.objectives = {}

    def add_variable(self, variable: Variable, name: str):
        self.variables[name] = variable

    def add_expression(self, expression: LinExpr, name: str):
        self.expressions[name] = expression
        # self.model.add_linear_expression(expression)

    def add_constraint(self, constraint: LinConstraint, name: str):
        self.constraints[name] = constraint
        # self.model.add_linear_constraint(constraint)
    
    def add_objective(self, objective: LinExpr, name: str):
        self.objectives[name] = objective
        # self.model.add_objective(objective, name)

    def add_var_model(self, variable: Variable, name: str):
        self.variables[name] = self.model.add_variable(variable)


class Element(ABC):
    period_elements: Dict[int, Dict[int, PeriodElement]]

    def __init__(self):
        self.period_elements = {}

    @property
    def interval_variables(self) -> List[Dict[str, List[Variable]]]:
        """ a list of variables across intervals for each scenario"""
        scenario_vars = []
        # scenario dict
        for _ , interval_element in self.period_elements.items():
            interval_vars: Dict[str, List[Variable]] = {}
            # interval dict
            for _ , period_element in interval_element.items():
                for var_name, variable in period_element.variables.items():
                    name = period_element.name + var_name
                    if name not in interval_vars:
                        interval_vars[name] = []
                    interval_vars[name].append(variable)
            scenario_vars.append(interval_vars)
            
        return scenario_vars
    
    
    def add_period_element(self, scenario: int, interval: int, period_element: PeriodElement) -> PeriodElement:
        if not  self.period_elements[scenario]:
            self.period_elements[scenario] = {}
        
        for name, variable in period_element.variables.items():
            variable.name = f"{variable.name}_scenario_{scenario}_interval_{interval}"
            period_element.add_var_model(variable, name)

        self.period_elements[scenario][interval] = period_element
        return period_element



    @classmethod
    def _is_period_element_collecton(cls, obj: Any) -> bool:
        """ 
        examines if object is of type Dict[int, Dict[int, PeriodElement]]
        assuming that the collections are homogenous
        """
        if not isinstance(obj, dict):
            return False
        # Get an example element from the top-level dictionary
        first_value = next(iter(obj.values()), None)
        if not isinstance(first_value, dict):
            return False
        # Get an example element from one of the second-level dictionaries
        first_inner_value = next(iter(first_value.values()), None)
        if not isinstance(first_inner_value, PeriodElement):
            return False

        return True


class AssetPeriod(PeriodElement):
    def __init__(self, interval: Interval, scenario: Scenario, variables: Dict[str, Variable], name: str):
        super().__init__()
        self.name = name
        self.interval = interval
        self.scenario = scenario
        for name , var in variables.items():
            self.add_variable(var, name)

class Asset(Element, PeriodElement):
    interval_power: Dict[int, Dict[int, AssetPeriod]]
    interval_energy: Dict[int, Dict[int, AssetPeriod]]

    def __init__(
        self,
        problem_param: Parameter,
        asset_param: AssetParam,
        asset_var: AssetVar,
    ):
        super().__init__()
        self.interval_power = {}
        self.interval_energy= {}
        for scenario in problem_param.scenarios:
            self.interval_power[scenario]= {}
            self.interval_energy[scenario] = {}
            for interval in problem_param.intervals:
                self.interval_power[scenario][interval] = self.add_period_element(
                    scenario,
                    interval, 
                    AssetPeriod(
                        interval,scenario, asset_var.power_vars, "interval_power"
                    ),
                )
            
                self.interval_energy[scenario][interval] =  self.add_period_element(
                    scenario,
                    interval, 
                    AssetPeriod(
                        interval,scenario, asset_var.power_vars, "interval_energy"
                    ),
                )
        
      


#  have Stage -> Scenaro -> Perod -> Interval
# what If we dont have any stage or scenario or period for a var
# what if  we have vars that are defined outside the intervals and stages
# techncally the root of the stage tree is stage_0
# we could start the stge count from one to show that 0 is for root 
# but at the same time we do index 0 for first inerval

# each var would have a unque name but can store it in the var 
# haveng a dct of   names and vars help to quickly know about what we are dealng with

# scenaro, interval nested or flat, we could create the other one from each
# what is the significance of the choice?


# so I am to define two most basic unit of compute, one that knows about intervals and sceanrios, and potentially child, parents, ...
# and one that only knows about opt objective, variables, constraints, etc.
# if we call the first component and the later element
# a coponent would know that we have a few  ElementPeriods or ComponentPeriods
# that involve an Interval and an Element
# the tricky part is that an ComponetPeriod is still an element and has multiple interval elements.w


# looks like we are makng an hidden (wrong!) assumption that the var_names will be Unique