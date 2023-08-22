from typing import TypeVar
from .service import Service



ServiceT = TypeVar("ServiceT", bound="Service")