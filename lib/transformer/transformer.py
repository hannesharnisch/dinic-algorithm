from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from lib.network.network import Network

T = TypeVar('T')
class Transformer(ABC, Generic[T]):
    @abstractmethod
    def transform(self, network: T) -> T:
        ...
