from lib.network.graph.identifiable import NodeID
from lib.network.network import Network
from lib.solver.solver import Solver
from lib.solver.solverState import SolverState


class DinicSolver(Solver):
    levels: dict[NodeID, int] = {}

    def solve(self, state: SolverState) -> SolverState:
        # TODO: implement Dinic Algorithm
        self.assign_levels_while_path_exists(network)
        path = self.get_path(network)
        print("path", path)
        print("Levels", self.levels)
        return SolverResult(network=network)

    def get_path(self, network: Network, source: NodeID = "s", sink: NodeID="t") -> list[NodeID]:
        path = []
        current_node = source
        path.append(current_node)
        while current_node != sink:
            for neighbor in network.neighbors(current_node):
                neighbor_arc = network.get_arc(current_node, neighbor.id)
                if self.levels[neighbor.id] == self.levels[current_node] + 1 and neighbor_arc.flow < neighbor_arc.capacity.ub:
                    path.append(neighbor.id)
                    current_node = neighbor.id
                    break
        return path
    
    
    def assign_levels_while_path_exists(self, network: Network, source: NodeID = "s", sink: NodeID = "t") -> bool:
        for n in network.nodes:
            self.levels[n.id] = -1
 
        # Level of source vertex
        self.levels[source] = 0
 
        # Create a queue, enqueue source vertex
        # and mark source vertex as visited here
        # level[] array works as visited array also
        q = []
        q.append(source)
        while q:
            current_node_id = q.pop(0)

            for neighbor in network.neighbors(current_node_id):
                neighbor_arc = network.get_arc(current_node_id, neighbor.id)
                print(neighbor_arc)

                if self.levels[neighbor.id] < 0 and neighbor_arc.flow < neighbor_arc.capacity.ub:
 
                    # Level of current vertex is
                    # level of parent + 1
                    self.levels[neighbor.id] = self.levels[current_node_id]+1
                    q.append(neighbor.id)
 
        # If we can not reach to the sink we
        # return False else True
        return False if self.levels[sink] < 0 else True