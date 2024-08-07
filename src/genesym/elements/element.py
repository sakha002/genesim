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

class Element(ABC):

    """
    An Element is an object that can add variables, expressions, constraints, or objectives
    to the model.
    """
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
        # NOTE: varable.name and name could be different
        # since the name should be unique in Element scope
        # variable.name should be unique in Model scope
        # I could come back to this, and see if just variable as argument would be enough
        
        self.variables[name] = variable

        interval_index = self.interval.index or 'null'
        scenario_index = self.scenario.index or 'null'

        variable.name =  f"{variable.name}_scenario_{scenario_index}_interval_{interval_index}"
        _ = self.model.add_variable(variable)
        # one approach would be to use self.interval and self.scenario here to add them to the model
        return

    def add_expression(self, expression: LinExpr, name: str):
        self.expressions[name] = expression
        # self.model.add_linear_expression(expression)

    def add_constraint(self, constraint: LinConstraint, name: str):
        self.constraints[name] = constraint
        # self.model.add_linear_constraint(constraint)
    
    def add_objective(self, objective: LinExpr, name: str):
        self.objectives[name] = objective
        # self.model.add_objective(objective, name)

    def get_element_vars_flat(self) -> Dict[str, Variable]:
        return {
            f"element_{self.name}_var_{name}": value for name, value in self.variables
        }



# when we add constraints/ or expressions to the Element, they need to have the variables
# attached to the model already
# but still the addition of constraints, and objectives, happen gradually,
# so expecting to pass all the items to the Element in init time is too much

# I also like the practice of Instantiating the Variables/Expressions, (including with Model)
# Separate From the Asset (ElementCollection)
# the benefit was that we could create a set of objectives/constraints for the asset, that would change
# depending on market, asset, iso, etc.

# so how to add variables to Element and to Model 
# seems we would need to add to model the same time.
# the dictionary that hold elment vars, and the one that holds model vars have diferent scope
# we could give the responsibility of adding interval/scenario indexes to the model at the element level
# or one above, i.e. the elementCollection