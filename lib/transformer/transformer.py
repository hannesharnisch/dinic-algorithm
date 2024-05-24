from abc import ABC, abstractmethod
from lib.network.network import Network


class Transformer(ABC):
    @abstractmethod
    def transform(self, network: Network) -> Network:
        ...
