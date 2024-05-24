

from lib.solver.solver import Solver
from lib.solver.solverResult import SolverResult


class GurobiNetworkSimplexSolver(Solver):

    def solve(self, network) -> SolverResult:
        initial_result = self.initial_result_solver.solve(network)
        #TODO: implement gurobi network simplex
        return SolverResult(network=initial_result.network, cost=0, flow=0)
        