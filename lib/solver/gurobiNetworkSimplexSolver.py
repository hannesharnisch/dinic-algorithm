

from lib.solver.solver import Solver
from lib.solver.solverState import SolverState


class GurobiNetworkSimplexSolver(Solver):

    def solve(self, network) -> SolverState:
        #initial_result = self.initial_result_solver.solve(network)
        #TODO: implement gurobi network simplex
        return SolverState(network=network)
        