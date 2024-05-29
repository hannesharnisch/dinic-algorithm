from lib.network.capacitatedArc import CapacitatedArc
from lib.network.network import Network
from lib.transformer.transformer import Transformer
import copy

class MinCostFlowTransformer(Transformer):
    def transform(self, network: Network) -> Network:
        """
        Function transforms a max-flow-network into a min-cost-flow-network

        The source node id must be "s" and the target node id must be "t"! 
        """
        networkCopy = copy.deepcopy(network)

        for arc in self.__getArcsFromSource(networkCopy.arcs):
            to_node = networkCopy.get_node(arc.to_node)
            to_node.demand = -arc.capacity # Set negative demand for node
            networkCopy.remove_arc(arc.from_node, arc.to_node)

        for arc in self.__getArcsToTarget(networkCopy.arcs):
            from_node = networkCopy.get_node(arc.from_node)
            from_node.demand = arc.capacity
            networkCopy.remove_arc(arc.from_node, arc.to_node)

        networkCopy.remove_node(networkCopy.get_node(0)) #TODO replace "s"
        networkCopy.remove_node(networkCopy.get_node(99)) #TODO replace "t"

        return networkCopy

    def __getArcsFromSource(self, arcs: list[CapacitatedArc]) -> list[CapacitatedArc]:
        return list(filter(lambda a: a.from_node == 0, arcs)) #TODO replace "s"
    
    def __getArcsToTarget(self, arcs: list[CapacitatedArc]) -> list[CapacitatedArc]:
        return list(filter(lambda a: a.to_node == 99, arcs)) #TODO replace "t"