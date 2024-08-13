from dataclasses import dataclass
from typing import List, Optional
from src.genesym.parameters.scenarios.scenario import Scenario
from src.genesym.parameters.scenarios.stage import Stage

@dataclass
class ScenarioGroup:
    scenarios: List[Scenario]
    stage: Optional[Stage] = None



@dataclass
class ScenarioInfo:
    scenario_groups: List[ScenarioGroup]


    @property
    def scenarios(self) -> List[Scenario]:
        return  self.get_stage_scenarios(0)


    def get_stage_scenarios(self, stage_index:int) -> List[Scenario]:
        return self.scenario_groups[stage_index].scenarios