from abc import ABC, abstractmethod

from lib.network.network import Network
from lib.solver.solverState import SolverState, SolverSolution

class Solver(ABC):
    @abstractmethod
    def solve(self, state: SolverState) -> SolverSolution:
        ...
