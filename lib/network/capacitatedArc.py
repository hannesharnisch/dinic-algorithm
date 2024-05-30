from dataclasses import dataclass
from typing import Tuple
from lib.network.graph.baseArc import BaseArc

@dataclass
class Capacity:
    ub:int
    lb:int = 0

@dataclass
class CapacitatedArc(BaseArc):
    capacity: Capacity
    cost: int
