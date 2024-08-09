from typing import Dict, List, TypeVar, Callable

from optclient.solver_utils.variable import Variable
from optclient.solver_utils.expression import LinExpr
from optclient.solver_utils.constraint import LinConstraint

from src.genesym.elements.element import Element
from src.genesym.elements.utils import ElementStore
from src.genesym.elements.types import ScenarioIndex, IntervIndex, ElementName

T = TypeVar('T')

class ElementGroup:

    """
    an ElementGroup is a group of elements, normally over a range of scnearios and a range of intervals
    we may have mutiple elements per scenaro/interval
    
    """
    name: str
    elements: ElementStore
    shared_elements: ElementStore

    def __init__(self):
        self.elements = ElementStore()

        # self.element_vars = ElementStore()
        # self.element_constraints = ElementStore()
        self.shared_elements = ElementStore()
        # self.shared_element_vars = ElementStore()

    
    def add_shared_element(self, scenario: int, interval: int, element: Element):
        """ 
        I add this for those elements that are meant to be shared,
        will see if we can create a public/pricvate element system
        """
        self.shared_elements.add_data(
            ScenarioIndex(scenario),
            IntervIndex(interval),
            ElementName(element.name),
            element,
        )
        # self.shared_element_vars.add_data(
        #     ScenarioIndex(scenario),
        #     IntervIndex(interval),
        #     ElementName(element.name),
        #     element.variables,
        # )
        
    def add_element(self, scenario: int, interval: int, element: Element):
        self.elements.add_data(
            ScenarioIndex(scenario),
            IntervIndex(interval),
            ElementName(element.name),
            element,
        )

        # self.element_vars.add_data(
        #     ScenarioIndex(scenario),
        #     IntervIndex(interval),
        #     ElementName(element.name),
        #     element.variables,
        # )

    def scenario_variable_list(self, scenario: int) -> Dict[str, List[Variable]]:
        """ a list of variables across intervals for each scenario"""

        return  self._flatten_element_attributes(scenario, lambda element: element.get_vars_flat())
    
    def scenario_expr_list(self, scenario: int) -> Dict[str, List[LinExpr]]:
        return self._flatten_element_attributes(scenario, lambda element: element.get_exprs_flat())
    
    def scenario_constr_list(self, scenario: int) -> Dict[str, List[LinConstraint]]:
        return self._flatten_element_attributes(scenario, lambda element: element.get_constrs_flat())
    
    def scenario_objective_list(self, scenario: int) -> Dict[str, List[LinExpr]]:
        return self._flatten_element_attributes(scenario, lambda element: element.get_objectives_flat())

    def _flatten_element_attributes(
        self,
        scenario: int,
        get_flat_fn: Callable[[Element], Dict[str, T]]
    ) -> Dict[str, List[T]]:
        
        flat_attr_dict: Dict[str, List[T]] = {}
        scenario_elements: Dict[ElementName, List[Element]] = self.elements.get_element_list_by_scenario(ScenarioIndex(scenario))
        
        for element_name, interval_list in scenario_elements.items():
            for interval_index, interval_element in enumerate(interval_list):
                for attr_name, attribute in get_flat_fn(interval_element).items():
                    if attr_name not in flat_attr_dict:
                        flat_attr_dict[attr_name] = [None] * len(interval_list)
                    
                    flat_attr_dict[attr_name][interval_index] = attribute
        
        return flat_attr_dict


# so before in the element store I was worried that 
# we are storing multiple elments with same name
# so I wouldn't want to use the element.name as name
# since elment.name of different elements could vary??
# but I think we could be okay considering that for example
# a number of elements all having the same name?
# okay I guess, for now!, we drop the rule of unique name for each element object.

# for name, variable in element.variables.items():
#     element.add_variable(variable, name)

# another question, when would be the process of adding elements, or defining element-groups
# I think we wanted to have the element creation and then adding stuff to it, to be independent
# so when you add an element to a element group, we could say that okay still keep it independent
# so essentially we would need to have the execuation of add_to_model for variables separate?
# but when we are adding stuff to the element, we should as well add them to model, since, 
# a whole bunch of expressions or constraints are not working without a model
# so again I have (1) create element, create element-group, add-element to element group
# and then add stuff to the element(variable, etc), and then at any point I could Ask for
# ElementGroup Variables, etc.
# but it will give me the variables, etc. added to that point.


# question, should I introduce the shared_elments/shared variale concept for the Elemet Group?
# the usage of the  ElementGroup is still not crystal clear to me
# would we be using them for an asset/product/assetgroup
# or for a feature of an Asset? like lets say Charge Var only?
# in it's current form (with shared elements maybe) I think it can be used for both
# But Last Time I Was thinking about it, I wanted to define an Asset For example 
# as a collection of Elments, and ELementGroups.
# if the Asset Itself becomes an ElmentGroup should work also
# the question is which way gives more advantage?
# why we go under so much trouble to define Battery Power Vars as an ElementGroup
# yeah it is more reasonable that the Asset Itself would be the ElementGroup