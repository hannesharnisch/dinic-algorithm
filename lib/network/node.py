from dataclasses import dataclass

from lib.network.graph.identifiable import Identifiable

@dataclass
class Node(Identifiable):
    demand: int = 0

    def __str__(self) -> str:
        return str(self.key) + " [Demand: " + self.demand + "]"