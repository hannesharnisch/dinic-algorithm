


from typing import Callable
from lib.network.network import Network
from lib.solver.solver import Solver
from lib.solver.solverResult import SolverResult
from lib.transformer.transformer import Transformer


class SolvingPipeline:
    __pipeline: list[Callable[[SolverResult], SolverResult]] = []
    
    def __init__(self, network: Network):
        self.network = network
        self.result = None

    def applySolver(self, solver: Solver) -> 'SolvingPipeline':
        return self.__add(lambda state: solver.solve(state.network))
    
    def transformNetwork(self, transformer: Transformer) -> 'SolvingPipeline':
        return self.__add(lambda state: SolverResult(transformer.transform(state.network), cost= state.cost, flow= state.flow))
    
    def __add(self, func: Callable[[SolverResult], SolverResult]) -> 'SolvingPipeline':
        self.__pipeline.append(func)
        return self

    def run(self) -> 'SolvingPipeline':
        state = SolverResult(self.network, cost=0, flow=0)
        for func in self.__pipeline:
            state = func(state)
        self.result = state
        return self