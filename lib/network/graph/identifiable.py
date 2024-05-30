from dataclasses import dataclass

type NodeID = str

@dataclass
class Identifiable:
    id: NodeID