from typing import Tuple
from lib.network.capacitatedArc import CapacitatedArc
from lib.network.graph.graph import Graph
from lib.network.node import Node
from lib.networkInput import NetworkInput


class Network(Graph[Node, CapacitatedArc]):
    def __init__(self, network_input: NetworkInput):
        super().__init__(network_input.nodes, network_input.arcs)