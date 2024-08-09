from collections import defaultdict
from typing import Dict, List, Any

from src.genesym.elements.types import ScenarioIndex, IntervIndex, ElementName


class ElementStore:
    def __init__(self):
        self._data: Dict[ScenarioIndex, Dict[IntervIndex, Dict[ElementName, Any]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
        self._interval_view: Dict[IntervIndex, Dict[ScenarioIndex, Dict[ElementName, Any]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
        self._name_view: Dict[ElementName, Dict[ScenarioIndex, Dict[IntervIndex, Any]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

        self._name_interval_list_view: Dict[ScenarioIndex, Dict[ElementName, List[Any]]] = defaultdict(lambda: defaultdict(list))
        self._name_scenario_list_view: Dict[IntervIndex, Dict[ElementName, List[Any]]] = defaultdict(lambda: defaultdict(list))
        self._scenario_interval_list_view: Dict[ElementName, Dict[ScenarioIndex, List[Any]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    def add_data(self, scenario: ScenarioIndex, interval: IntervIndex, name: ElementName, value: Any):
        self._data[scenario][interval][name] = value
        self._update_views(scenario, interval, name, value)
    
    def _update_views(self, scenario: ScenarioIndex, interval: IntervIndex, name: ElementName, value: Any):
        self._interval_view[interval][scenario][name] = value
        self._name_view[name][scenario][interval] = value

        self._name_interval_list_view[scenario][name].append(value)
        self._name_scenario_list_view[interval][name].append(value)
        self._scenario_interval_list_view[name][scenario].append(value)

    def get_scenario_view(self) ->  Dict[ScenarioIndex, Dict[IntervIndex, Dict[ElementName, Any]]]:
        return self._data

    def get_interval_view(self) -> Dict[IntervIndex, Dict[ScenarioIndex, Dict[ElementName, Any]]]:
        return self._interval_view
    
    def get_name_view(self) ->  Dict[ElementName, Dict[ScenarioIndex, Dict[IntervIndex, Any]]]:
        return self._name_view

    def get_elments(self, scenario: ScenarioIndex, interval: IntervIndex,) -> Dict[ElementName, Any]:
        return self._data[scenario][interval]

    def get_elements_by_scenario(self, scenario: ScenarioIndex) -> Dict[IntervIndex, Dict[ElementName, Any]]:
        return self._data[scenario]
    
    def get_elements_by_interval(self, interval: IntervIndex,) -> Dict[ScenarioIndex, Dict[ElementName, Any]]:
        return self._interval_view[interval]
    
    def get_element_by_name(self, name: ElementName) -> Dict[ScenarioIndex, Dict[IntervIndex, Any]]:
        return self._name_view[name]
    
    def get_element_list_by_scenario(self, scenario: ScenarioIndex) -> Dict[ElementName, List[Any]]:
        return self._name_interval_list_view[scenario]

    def get_element_list_by_scenario_name(self, scenario: ScenarioIndex, name: ElementName) -> List[Any]:
        return self._name_interval_list_view[scenario][name]
    
    def get_element_list_by_interval(self, interval: IntervIndex) -> Dict[ElementName, List[Any]]:
        return self._name_scenario_list_view
    
    def get_element_list_by_interval_name(self,  interval: IntervIndex, name: ElementName) -> List[Any]:
        return self._name_scenario_list_view[interval][name]
    
    def get_element_list_by_name(self, name: ElementName) -> Dict[ScenarioIndex, List[Any]]:
        return self._scenario_interval_list_view[name]
    

    



