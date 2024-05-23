

from lib.solver.solver import Solver
from lib.solver.solverResult import SolverResult


class GurobiNetworkSimplexSolver(Solver):
    def __init__(self, initial_result_solver: Solver):
        self.initial_result_solver = initial_result_solver

    def solve(self, network) -> SolverResult:
        initial_result = self.initial_result_solver.solve(network)
        #TODO: implement gurobi network simplex
        return SolverResult(network=initial_result.network, cost=0, flow=0)
        