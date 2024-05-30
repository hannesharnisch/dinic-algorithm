from abc import ABC
from typing import Callable, Type
from lib.network.graph.identifiable import NodeID
from lib.network.network import Network
from lib.solver.solver import Solver
from lib.solver.solverResult import SolverResult


class DinicSolver(Solver):
    levels: dict[NodeID, int] = {}

    def solve(self, network: Network) -> SolverResult:
        # TODO: implement Dinic Algorithm

        return SolverResult(network=network, cost=0, flow=0)
    
    def assign_levels_while_path_exists(self, network: Network, source: NodeID = "s", sink: NodeID = "t") -> bool:
        for n in network.nodes:
            self.levels[n] = -1
 
        # Level of source vertex
        self.levels[source] = 0
 
        # Create a queue, enqueue source vertex
        # and mark source vertex as visited here
        # level[] array works as visited array also
        q = []
        q.append(source)
        while q:
            u = q.pop(0)
            for i in range(len(network.neighbors[u])):
                e = network.get_arc(u, i)
                if self.levels[e.id] < 0 and e.flow < e.capacity.ub:
 
                    # Level of current vertex is
                    # level of parent + 1
                    self.levels[e.id] = self.levels[u]+1
                    q.append(e.id)
 
        # If we can not reach to the sink we
        # return False else True
        return False if self.levels[sink] < 0 else True