

import copy
from dataclasses import dataclass
from typing import Callable

from loguru import logger
from lib.exporter.exporter import Exporter
from lib.network.network import Network
from lib.solver.solver import Solver
from lib.solver.solverState import SolverState, SolverSolution
from lib.transformer.transformer import Transformer


@dataclass
class Pipe:
    name: str
    func: Callable[[SolverState], SolverState]

    def apply(self, state: SolverState) -> SolverState:
        try:
            logger.debug("Running pipe: " + self.name)
            logger.debug("Network: \n" +
                         "\n".join(map(str, state.network.arcs)))
            if state.solution:
                logger.debug("Solution: \n" + str(state.solution))

            new_state = self.func(state)
            if new_state == None:
                logger.info(
                    f"Pipe {self.name} returned no new result - continuing with old state.")
                return state

            logger.debug("New Network: \n" +
                         "\n".join(map(str, new_state.network.arcs)))
            if new_state.solution:
                logger.debug("New Solution: \n" + str(new_state.solution))

            return new_state
        except Exception as e:
            raise Exception(f"Error in pipe {self.name}: \n{e}")


class SolvingPipeline:

    def __init__(self, network: Network):
        self.__pipeline: list[Pipe] = []
        self.network = network
        self.result = None

    def apply_solver(self, solver: Solver) -> 'SolvingPipeline':
        return self.__add(
            name="Solver-" + type(solver).__name__,
            func=lambda state: solver.solve(state)
        )

    def export_to_file(self, exporter: Exporter, file_name: str) -> 'SolvingPipeline':
        return self.__add(
            name="Plotter-" + type(Exporter).__name__,
            func=lambda state: exporter.export(
                file_name=file_name, state=state)
        )

    def transform_network(self, transformer: Transformer[Network]) -> 'SolvingPipeline':
        return self.__add(
            name="Networktransformer-" + type(transformer).__name__,
            func=lambda state: SolverState(
                transformer.transform(state.network), state.solution)
        )

    def transform_solution(self, transformer: Transformer[SolverSolution]) -> 'SolvingPipeline':
        return self.__add(
            name="Solutiontransformer-" + type(transformer).__name__,
            func=lambda state: SolverState(
                state.network, transformer.transform(state.solution))
        )

    def use_initial_network(self) -> 'SolvingPipeline':
        return self.__add(
            name="Use Initial Network",
            func=lambda state: SolverState(network=copy.deepcopy(
                self.network), solution=state.solution)
        )

    def __add(self, name: str, func: Callable[[SolverState], SolverState]) -> 'SolvingPipeline':
        self.__pipeline.append(Pipe(name=name, func=func))
        return self

    def run(self) -> 'SolvingPipeline':
        state = SolverState(copy.deepcopy(self.network))
        logger.debug("Starting SolvingPipeline for network: \n" +
                     "\n".join(map(str, state.network.arcs)))
        for pipe in self.__pipeline:
            state = pipe.apply(state)
        logger.debug("Finished SolvingPipeline with network: \n" +
                     "\n".join(map(str, state.network.arcs)))
        self.result = state
        return self
