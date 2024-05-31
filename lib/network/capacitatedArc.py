from dataclasses import dataclass
from typing import Optional, Tuple
from lib.network.graph.baseArc import BaseArc

@dataclass
class Capacity:
    ub:int
    lb:int = 0

@dataclass
class CapacitatedArc(BaseArc):
    capacity: Capacity
    cost: int
    flow: Optional[int] = 0

    def __str__(self) -> str:
        return f"{self.from_node} -> {self.to_node} (lb={self.capacity.lb}, ub={self.capacity.ub}, c={self.cost})"
