from dataclasses import dataclass
from lib.network.graph.identifiable import Identifiable, NodeID

@dataclass
class BaseArc:
    from_node: NodeID
    to_node: NodeID