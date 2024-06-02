import copy
from math import inf
from typing import Tuple
from lib.network.capacitatedArc import CapacitatedArc, Capacity
from lib.network.graph.identifiable import NodeID
from lib.network.network import Network
from lib.solver.solver import Solver
from lib.solver.solverState import SolverSolution, SolverState


class DinicSolver(Solver):
    levels: dict[NodeID, int] = {}
    dinic_network: Network

    def solve(self, state: SolverState) -> SolverState:

        self.dinic_network = copy.deepcopy(state.network)
        total_flow = 0.0


        while self.assign_levels_while_path_exists():

            path = self.rek_get_path()
            max_flow = self.get_max_flow(path)
            self.load_path(path, max_flow)

            total_flow += max_flow
        
        flow = self.get_final_flow()
     
        return SolverState(network=state.network, solution=SolverSolution(flow=flow, target_value=total_flow))
    
    def get_final_flow(self) -> dict[Tuple[NodeID, NodeID], int]:

        res = {}

        for arc in self.dinic_network.arcs:
            if arc.flow < 0:
                res[(arc.to_node, arc.from_node)] = abs(arc.flow)

        return res
  
    def rek_get_path(self, source: NodeID = "s", sink: NodeID="t") -> list[NodeID]:
        if source == sink:
            return []
        for neighbor in self.dinic_network.neighbors(source):
            neighbor_arc = self.dinic_network.get_arc(source, neighbor.id)
            if self.levels[neighbor.id] == self.levels[source] + 1 and neighbor_arc.flow < neighbor_arc.capacity.ub:
                path = self.rek_get_path(neighbor.id, sink)
                if path is not None:
                    path.insert(0, neighbor_arc)
                    return path
        return None
    
    def get_max_flow(self, path: list[CapacitatedArc]) -> None:
        
        ub = inf
        lb = -inf

        for arc in path:
            if arc.capacity.ub < ub:
                ub = arc.capacity.ub - arc.flow
            if arc.capacity.lb < lb:
                lb = arc.capacity.lb + arc.flow

        # ToDo: Check if lb < ub
        if ub < lb: 
            raise Exception

        return ub
    
    def load_path(self, path: list[CapacitatedArc], flow: int) -> None:
        for arc in path:
            arc.flow += flow
            try :
                reverse_arc = self.dinic_network.get_arc(arc.to_node, arc.from_node)
                reverse_arc.flow -= flow
            except ValueError:
                reverse_arc = CapacitatedArc(from_node=arc.to_node, to_node=arc.from_node, capacity=Capacity(-arc.capacity.lb,-arc.capacity.ub),flow=-flow, cost=arc.cost)
                self.dinic_network.add_arc(reverse_arc)
    
    
    def assign_levels_while_path_exists(self, source: NodeID = "s", sink: NodeID = "t") -> bool:
        for n in self.dinic_network.nodes:
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

            for neighbor in self.dinic_network.neighbors(current_node_id):
                neighbor_arc = self.dinic_network.get_arc(current_node_id, neighbor.id)


                if self.levels[neighbor.id] < 0 and abs(neighbor_arc.flow) < neighbor_arc.capacity.ub:
 
                    # Level of current vertex is
                    # level of parent + 1
                    self.levels[neighbor.id] = self.levels[current_node_id]+1
                    q.append(neighbor.id)
 
        # If we can not reach to the sink we
        # return False else True
        return False if self.levels[sink] < 0 else True