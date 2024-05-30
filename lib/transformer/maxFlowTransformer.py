from lib.network.network import Network
from lib.network.network import Node
from lib.network.network import CapacitatedArc
from lib.transformer.transformer import Transformer
import copy
import math

class MaxFlowTransformer(Transformer):
    def transform(self, network: Network) -> Network:
        """
        Function should get a min-cost-flow-network and convert it into a max-flow-network

        The source node id will be "s" and the target node id will be "t"! 
        """
        # Other option for inf is sys.maxsize
        startNode = Node("s", -math.inf)
        endNode = Node("t", math.inf)

        networkCopy = copy.deepcopy(network)

        networkCopy.add_node(startNode)
        networkCopy.add_node(endNode)

        for n in networkCopy.nodes:
            if n.id == "s" or n.id == "t":
                continue
            
            if n.demand < 0:
                # Add arc from source
                networkCopy.add_arc(CapacitatedArc("s", n.id, abs(n.demand), 0))

            if n.demand > 0:
                #Add arc to target
                networkCopy.add_arc(CapacitatedArc(n.id, "t", n.demand, 0))
            
            n.demand = 0 # Set demand to 0

        return networkCopy

