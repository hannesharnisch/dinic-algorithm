from lib.network.network import Network
from lib.network.network import Node
from lib.network.network import CapacitatedArc
from lib.transformer.transformer import Transformer
import copy

class MaxFlowTransformer(Transformer):
    def transform(self, network: Network) -> Network:
        """
        Function should get a min-cost-flow-network and convert it into a max-flow-network

        The source node id will be "s" and the target node id will be "t"! 
        """
        simulated_infinity = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        simulated_negative_infinity = -simulated_infinity

        startNode = Node(0, simulated_negative_infinity) # TODO set to "s"
        endNode = Node(99, simulated_infinity) # TODO set to "t"

        networkCopy = copy.deepcopy(network)

        networkCopy.add_node(startNode)
        networkCopy.add_node(endNode)

        for n in networkCopy.nodes:
            if n.id == 0 or n.id == 99: #TODO set 0 to "s"
                continue
            
            if n.demand < 0:
                # Add arc from source
                networkCopy.add_arc(CapacitatedArc(0, n.id, abs(n.demand))) #TODO set 0 to "s"

            if n.demand > 0:
                #Add arc to target
                networkCopy.add_arc(CapacitatedArc(n.id, 99, n.demand)) # TODO set 99 to "t"
            
            n.demand = 0 # Set demand to 0

        return networkCopy

