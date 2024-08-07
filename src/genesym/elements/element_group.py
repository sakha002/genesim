from typing import Dict, List

from optclient.solver_utils.variable import Variable

from src.genesym.elements.element import Element

class ElementGroup:

    """
    an ElementGroup is a group of elements, normally over a range of scnearios and a range of intervals
    we may have mutiple elements per scenaro/interval
    
    """
    name: str
    elements: Dict[int, Dict[int, Dict[str, Element]]]

    def __init__(self):
        self.elements = {}
    

        
    def add_element(self, scenario: int, interval: int, element: Element) -> Element:
        if not  self.elements[scenario]:
            self.elements[scenario] = {}
        
        # for name, variable in element.variables.items():
        #     element.add_variable(variable, name)

        if not self.elements[scenario][interval]:
            self.elements[scenario][interval] = {}

        self.elements[scenario][interval][element.name] = element
        return element

    @property
    def interval_variables(self) -> List[Dict[str, List[Variable]]]:
        """ a list of variables across intervals for each scenario"""
        scenario_vars = []
        # scenario dict
        for scenario_element in self.elements.values():
            interval_vars: Dict[str, List[Variable]] = {}
            # interval dict
            for interval_element in scenario_element.values():
                for element in interval_element.values():
                    element_vars = element.get_element_vars_flat()
                    for var_name_extended, var in element_vars.items():
                        if not var_name_extended in interval_vars:
                            interval_vars[var_name_extended] = []
                        


                    # for var_name, variable in element.variables.items():
                    #     var_name_extended = element_name + var_name
                    #     if not var_name_extended in interval_vars:
                    #         interval_vars[var_name_extended] = []
                        




                for var_name, variable in period_element.variables.items():
                    name = period_element.name + var_name
                    if name not in interval_vars:
                        interval_vars[name] = []
                    interval_vars[name].append(variable)
            scenario_vars.append(interval_vars)
            
        return scenario_vars
    





