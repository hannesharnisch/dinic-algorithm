from lib.network.network import Network
from lib.solver.solver import Solver
from lib.solver.solverState import SolverState
import gurobipy as gp


class GurobiMaxFlowSolver(Solver):
    def solve(self, state: SolverState) -> SolverState:
        # TODO: implement Max Flow Solver
        return state