from typing import Optional

from dataclasses import dataclass



@dataclass
class AssetPeriod:
    
    p_out_max: Optional[float] = None
    p_out_min: float = 0.0
    p_in_max: Optional[float] = None
    p_in_min: float = 0.0
    e_out_max: Optional[float] = None
    e_out_min: float = 0.0
    e_in_max: Optional[float] = None
    e_in_min: float = 0.0


