import os
from loguru import logger
import networkx as nx
import matplotlib.pyplot as plt

from lib.exporter.exporter import Exporter
from lib.solver.solverState import SolverState


class PlotExporter(Exporter):
    def __init__(self):
        pass

    def export(self, state: SolverState, file_name: str, title: str = None) -> SolverState:

        G = nx.DiGraph()
        edge_list_solution, edge_list_unused, edge_list_back = [], [], []

        node_size = 800

        plt.figure(figsize=(15, 15))

        for arc in state.network.arcs:
            if state.solution:
                if (arc.from_node, arc.to_node) in state.solution.flow:

                    flow = f"({state.solution.flow[arc.from_node, arc.to_node]}," \
                        f" {arc.capacity.ub})"
                    edge_list_solution.append((arc.from_node, arc.to_node))
                else:
                    flow = 0
                    edge_list_unused.append((arc.from_node, arc.to_node))

            else:
                if arc.flow > 0:
                    flow = f"({arc.flow}, {arc.capacity.ub})"
                    edge_list_solution.append((arc.from_node, arc.to_node))
                elif arc.flow < 0:
                    flow = f"({arc.flow}, {arc.capacity.ub})"
                    edge_list_back.append((arc.from_node, arc.to_node))
                else:
                    flow = f""
                    edge_list_unused.append((arc.from_node, arc.to_node))

            G.add_edge(arc.from_node, arc.to_node, flow=flow)

        pos = nx.kamada_kawai_layout(G)

        nx.draw_networkx_nodes(G, pos, node_size=node_size)

        connectionstyle = "arc3"
        if len(edge_list_back) > 0:
            connectionstyle = "arc3,rad=0.3"

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=edge_list_solution,
            arrowstyle='->',
            arrows=True,
            node_size=node_size,
            style='solid',
            connectionstyle=connectionstyle,
        )

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=edge_list_back,
            arrowstyle='->',
            arrows=True,
            node_size=node_size,
            style='solid',
            connectionstyle=connectionstyle,
            edge_color='blue'
        )

        nx.draw_networkx_edges(
            G,
            pos,
            arrowstyle='->',
            edgelist=edge_list_unused,
            arrows=True,
            node_size=node_size,
            style='dashed',
        )

        nx.draw_networkx_labels(G, pos, font_color='white')

        # get edge and node attributes
        edge_labels = nx.get_edge_attributes(G, 'flow')

        # draw edge attributes
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, connectionstyle=connectionstyle)

        plt.text(1, 0, '(Flow, Upper Bound)', horizontalalignment='right',
                 verticalalignment='bottom', transform=plt.gca().transAxes)

        if title:
            plt.title(title)

        if state.solution:
            plt.suptitle("Target Value: " + str(state.solution.target_value))

        file_path = f'./Output/{file_name}.png'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        plt.savefig(file_path)

        plt.clf()

        return state
