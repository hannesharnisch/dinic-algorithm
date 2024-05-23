from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar

type NodeID = int

@dataclass
class Identifiable(ABC):
    id: NodeID