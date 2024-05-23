from abc import ABC, abstractmethod

from lib.network.network import Network
from lib.solver.solverResult import SolverResult

class Solver(ABC):
    @abstractmethod
    def solve(self, network: Network) -> SolverResult:
        ...
