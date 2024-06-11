import copy
from datetime import datetime
from math import inf
from typing import Tuple

from loguru import logger
from lib.settings import settings
from lib.exporter.plotExporter import PlotExporter
from lib.network.capacitatedArc import CapacitatedArc, Capacity
from lib.network.graph.identifiable import NodeID
from lib.network.network import Network
from lib.solver.solver import Solver
from lib.solver.solverState import SolverSolution, SolverState


class DinicSolver(Solver):
    levels: dict[NodeID, int] = {}
    dinic_network: Network

    def plot(self, iteration: int) -> None:
        PlotExporter().export(SolverState(network=self.dinic_network,
                                          solution=None), f"/Dinic/Steps/iteration_{iteration}", f"Dinic - Iteration {iteration}")

    def solve(self, state: SolverState) -> SolverState:
        self.dinic_network = copy.deepcopy(state.network)

        start = datetime.now()

        total_flow = 0.0
        i = 1

        while self.assign_levels_while_path_exists():

            # path = self.rek_get_path()

            path = self.get_path()
            max_flow = self.get_max_flow(path)
            self.load_path(path, max_flow)

            total_flow += max_flow

            if settings.plot_dinic_steps:
                self.plot(i)

            i += 1

        flow = self.get_final_flow()

        end = datetime.now()

        logger.info(f"Iterations: {i}")

        logger.success(f"Dinic - Calculation duration: {end-start}")

        return SolverState(network=state.network, solution=SolverSolution(flow=flow, target_value=total_flow, calc_duration=end-start))

    def get_final_flow(self) -> dict[Tuple[NodeID, NodeID], int]:

        res = {}

        for arc in self.dinic_network.arcs:
            if arc.flow < 0:
                res[(arc.to_node, arc.from_node)] = abs(arc.flow)

        return res

    def get_path(self, source: NodeID = "s", sink: NodeID = "t") -> list[CapacitatedArc]:
        stack = [(source, [])]  # Stack to store the current path and source
        visited = set()  # Store already visited nodes
        while stack:
            current_node, path = stack.pop()

            if current_node == sink:
                return path

            visited.add(current_node)

            for neighbor in self.dinic_network.neighbors(current_node):
                neighbor_arc = self.dinic_network.get_arc(
                    current_node, neighbor.id)
                if neighbor.id not in current_node and self.levels[neighbor.id] == self.levels[current_node] + 1 and neighbor_arc.flow < neighbor_arc.capacity.ub:
                    stack.append((neighbor.id, path + [neighbor_arc]))

        return None

    def rek_get_path(self, source: NodeID = "s", sink: NodeID = "t") -> list[CapacitatedArc]:
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
            try:
                reverse_arc = self.dinic_network.get_arc(
                    arc.to_node, arc.from_node)
                reverse_arc.flow -= flow
            except ValueError:
                reverse_arc = CapacitatedArc(from_node=arc.to_node, to_node=arc.from_node, capacity=Capacity(
                    -arc.capacity.lb, -arc.capacity.ub), flow=-flow, cost=arc.cost)
                self.dinic_network.add_arc(reverse_arc)

    def assign_levels_while_path_exists(self, source: NodeID = "s", sink: NodeID = "t") -> bool:
        for n in self.dinic_network.nodes:
            self.levels[n.id] = -1

        self.levels[source] = 0

        q = []
        q.append(source)
        while q:
            current_node_id = q.pop(0)

            for neighbor in self.dinic_network.neighbors(current_node_id):
                neighbor_arc = self.dinic_network.get_arc(
                    current_node_id, neighbor.id)

                if self.levels[neighbor.id] < 0 and abs(neighbor_arc.flow) < neighbor_arc.capacity.ub:

                    self.levels[neighbor.id] = self.levels[current_node_id]+1
                    q.append(neighbor.id)

        return self.levels[sink] != -1
