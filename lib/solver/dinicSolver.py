from abc import ABC
from typing import Type
from lib.network.network import Network
from lib.solver.solver import Solver
from lib.solver.solverResult import SolverResult


class DinicSolver(Solver):
    def solve(self, network: Network) -> SolverResult:
        # TODO: implement Dinic Algorithm
        return SolverResult(network=network, cost=0, flow=0)