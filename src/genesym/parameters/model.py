from dataclasses import dataclass
from typing import TypeVar

from src.genesym.parameters.horizons.horizon import Horizon
from src.genesym.parameters.scenarios.scenario_group import ScenarioInfo



@dataclass
class ParamModel:
    horizon: Horizon
    scenario_info: ScenarioInfo


ParamModelT = TypeVar('ParamModelT', bound=ParamModel)