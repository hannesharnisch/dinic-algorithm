from typing import Tuple, TypeVar, Generic
from lib.network.graph.identifiable import NodeID
from lib.network.graph.baseArc import BaseArc
from lib.network.graph.identifiable import Identifiable

N = TypeVar('N', bound=Identifiable)
A = TypeVar('A', bound=BaseArc)

class Graph(Generic[N, A]):
    __nodes: dict[NodeID, N] = {}
    __arcs: dict[Tuple[NodeID, NodeID], A] = {}
    __adjacency_list: dict[NodeID, list[NodeID]] = {}

    def __init__(self, nodes: list[N] = [], arcs: list[A] = []):
        for node in nodes:
            self.add_node(node)
        for arc in arcs:
            self.add_arc(arc)
    @property
    def nodes(self) -> list[N]:
        return self.__nodes.values()

    @property
    def arcs(self) -> list[A]:
        return self.__arcs.values()
    
    def get_node(self, node_NodeID: NodeID) -> N:
        if node_NodeID not in self.__nodes:
            raise ValueError('Node not found')
        
        return self.__nodes[node_NodeID]
    
    def add_node(self, node: N):
        self.__nodes[node.NodeID] = node

    def remove_node(self, node: N):
        self.__nodes.pop(node.NodeID)
        for arc in self.__arcs.values():
            if arc.from_node == node.NodeID or arc.to_node == node.NodeID:
                self.remove_arc((arc.from_node, arc.to_node))
        for key, adjacent_nodes in self.__adjacency_list.items():
            if node.NodeID in adjacent_nodes:
                self.__adjacency_list[key].remove(node.NodeID)
        self.__adjacency_list.pop(node.NodeID)


    def get_arc(self, from_node: NodeID, to_node: NodeID) -> A:
        if (from_node, to_node) not in self.__arcs:
            raise ValueError('Arc not found')
        
        return self.__arcs[(from_node, to_node)]

    def add_arc(self, arc: A):
        if arc.from_node not in self.nodes or arc.to_node not in self.nodes:
            raise ValueError('Arc contains invalNodeID node')

        self.__arcs[(arc.from_node, arc.to_node)] = arc
        self.__adjacency_list[arc.from_node].append(arc.to_node)

    def remove_arc(self, from_node: NodeID, to_node: NodeID):
        self.__arcs.pop((from_node, to_node))
        self.__adjacency_list[from_node].remove(to_node)

    def is_adjacent(self, from_node: NodeID, to_node: NodeID) -> bool:
        return to_node in self.__adjacency_list[from_node]
    
    def neighbors(self, node_NodeID: NodeID) -> list[N]:
        return self.__adjacency_list[node_NodeID].map(lambda x: self.__nodes[x])