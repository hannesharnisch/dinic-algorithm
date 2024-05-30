import json
from lib.network.capacitatedArc import CapacitatedArc, Capacity
from lib.network.node import Node


class NetworkInput:
    def __init__(self):
        self.nodes: list[Node] = []
        self.arcs: list[CapacitatedArc] = []
    
    def load_data_from_txt_file(self, data_path_and_name: str) :
        with open(data_path_and_name, 'r') as file:
            data = json.load(file)
            for node, value in data['nodes'].items():
                self.nodes.append(Node(node, value['demand']))
            for arc in data['arcs']:
                capacity = Capacity(ub=arc['upper_bound'], lb=arc['lower_bound'])
                self.arcs.append(CapacitatedArc(arc['from'], arc['to'], capacity, arc['cost']))



