from dataclasses import dataclass

from src.genesym.parameters.horizons.horizon import Horizon

@dataclass
class ModelParams:
    horizon: Horizon
    # scenario: 