from dataclasses import dataclass
from typing import   List

from src.genesym.parameters.horizons.horizon import Horizon
from src.genesym.parameters.scenarios.scenario_group import ScenarioInfo



@dataclass
class ModelParam:
    horizon: Horizon
    scenario_info: ScenarioInfo