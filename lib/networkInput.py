import json
from lib.network.capacitatedArc import CapacitatedArc
from lib.network.node import Node


class NetworkInput:
    nodes: list[Node] = []
    arcs: list[CapacitatedArc] = []
    
    def load_data_from_txt_file(self, data_path_and_name: str) :
        with open(data_path_and_name, 'r') as file:
            data = json.load(file)
            for node in data['nodes']:
                self.nodes.append(node)
            for arc in data['arcs']:
                self.arcs.append(arc)



