from lib.network.network import Network
from lib.solver.solver import Solver
from lib.solver.solverResult import SolverResult
import gurobipy as gp


class GurobiMaxFlowSolver(Solver):
    def solve(self, network: Network) -> SolverResult:
        # TODO: implement Max Flow Solver
        return SolverResult(network=network)