


import copy
from typing import Callable
from lib.network.network import Network
from lib.solver.solver import Solver
from lib.solver.solverState import SolverState, SolverSolution
from lib.transformer.transformer import Transformer


class SolvingPipeline:
    __pipeline: list[Callable[[SolverState], SolverState]] = []
    
    def __init__(self, network: Network):
        self.network = network
        self.result = None

    def apply_solver(self, solver: Solver) -> 'SolvingPipeline':
        return self.__add(lambda state: solver.solve(state))
    
    def transform_network(self, transformer: Transformer[Network]) -> 'SolvingPipeline':
        return self.__add(lambda state: SolverState(transformer.transform(state.network), state.solution))
    
    def transform_solution(self, transformer: Transformer[SolverSolution]) -> 'SolvingPipeline':
        return self.__add(lambda state: SolverState(state.network, transformer.transform(state.solution)))
    
    def use_initial_network(self) -> 'SolvingPipeline':
        return self.__add(lambda state: SolverState(network=copy.deepcopy(self.network), solution=state.solution))

    def __add(self, func: Callable[[SolverState], SolverState]) -> 'SolvingPipeline':
        self.__pipeline.append(func)
        return self

    def run(self) -> 'SolvingPipeline':
        state = SolverState(copy.deepcopy(self.network))
        for func in self.__pipeline:
            new_state = func(state)
            state = new_state if new_state != None else state
        self.result = state
        return self