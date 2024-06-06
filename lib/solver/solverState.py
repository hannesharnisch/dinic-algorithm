from dataclasses import dataclass
import datetime
from lib.network.network import Network
from typing import Tuple
from lib.network.graph.identifiable import NodeID


@dataclass
class SolverSolution:
    flow: dict[Tuple[NodeID, NodeID], int]
    target_value: float = 0
    calc_duration: datetime.timedelta = None

    def __str__(self) -> str:
        return "Target: " + str(self.target_value) + ", Flow: " + str(self.flow)


@dataclass
class SolverState:
    network: Network
    solution: SolverSolution = None

    def __str__(self) -> str:
        return "Network: " + str(self.network.arcs) + ", " + str(self.solution)
