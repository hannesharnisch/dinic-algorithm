from dataclasses import dataclass
from lib.network.graph.identifiable import Identifiable

@dataclass
class BaseArc:
    from_node: int
    to_node: int