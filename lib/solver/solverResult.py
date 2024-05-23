from dataclasses import dataclass
from lib.network.network import Network

@dataclass
class SolverResult:
    network: Network
    cost: int
    flow: int
    
    def __str__(self) -> str:
        return "Network: " + str(self.network.arcs) + " Cost: " + str(self.cost) + " Flow: " + str(self.flow)