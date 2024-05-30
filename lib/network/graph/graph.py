import copy
from typing import Tuple, TypeVar, Generic
from lib.network.graph.identifiable import NodeID
from lib.network.graph.baseArc import BaseArc
from lib.network.graph.identifiable import Identifiable

N = TypeVar('N', bound=Identifiable)
A = TypeVar('A', bound=BaseArc)

class Graph(Generic[N, A]):

    def __init__(self, nodes: list[N] = [], arcs: list[A] = []):
        self.__nodes: dict[NodeID, N] = {}
        self.__arcs: dict[Tuple[NodeID, NodeID], A] = {}
        self.__adjacency_list: dict[NodeID, list[NodeID]] = {}
        
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
    
    def get_node(self, node_id: NodeID) -> N:
        if node_id not in self.__nodes:
            raise ValueError('Node not found')
        
        return self.__nodes[node_id]
    
    def add_node(self, node: N):
        self.__nodes[node.id] = node
        self.__adjacency_list[node.id] = []

    def remove_node(self, node: N):
        self.__nodes.pop(node.id)
        arcs_to_remove = filter(lambda arc: arc.from_node == node.id or arc.to_node == node.id, self.__arcs.values())
        for arc in list(arcs_to_remove):
            self.remove_arc(arc.from_node, arc.to_node)
        self.__adjacency_list.pop(node.id)


    def get_arc(self, from_node: NodeID, to_node: NodeID) -> A:
        if (from_node, to_node) not in self.__arcs:
            raise ValueError('Arc not found')
        
        return self.__arcs[(from_node, to_node)]

    def add_arc(self, arc: A):
        if arc.from_node not in self.__nodes or arc.to_node not in self.__nodes:
            raise ValueError('Arc contains invalid node')

        self.__arcs[(arc.from_node, arc.to_node)] = arc
        self.__adjacency_list[arc.from_node].append(arc.to_node)

    def remove_arc(self, from_node: NodeID, to_node: NodeID):
        self.__arcs.pop((from_node, to_node))
        self.__adjacency_list[from_node].remove(to_node)

    def is_adjacent(self, from_node: NodeID, to_node: NodeID) -> bool:
        return to_node in self.__adjacency_list[from_node]
    
    def neighbors(self, node_id: NodeID) -> list[N]:
        return [self.__nodes[id] for id in self.__adjacency_list[node_id]] 