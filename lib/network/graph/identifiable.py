from abc import ABC
from dataclasses import dataclass

type NodeID = str

@dataclass
class Identifiable(ABC):
    id: NodeID