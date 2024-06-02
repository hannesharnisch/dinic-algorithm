from abc import ABC, abstractmethod

from lib.solver.solverState import SolverState

class Exporter(ABC):
    @abstractmethod
    def export(self, state: SolverState, file_name:str) -> SolverState:
        ...
