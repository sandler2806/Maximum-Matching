from typing import List

from Graph import Graph
from Node import Node
import copy


class MaximumMatching:

    def __init__(self, graph: Graph):
        self.orgGraph = graph
        self.graph = graph
        self.cycle: List[Node] = []

    def constract_blossom(self, blossom_nodes: list):
        self.cycle = blossom_nodes
        blossom: Node = copy.deepcopy(blossom_nodes[0])
        blossom.clear_node()
        self.graph.nodes[blossom.key] = blossom
        for node in blossom_nodes:
            for edge in node.edges:
                temp_node: Node = self.orgGraph.nodes.get(edge)
                if temp_node not in blossom_nodes:
                    if temp_node.key not in blossom.edges:
                        self.graph.add_edge(blossom.key, temp_node.key)
                    if node.match == temp_node:
                        blossom.match = temp_node
        for node in blossom_nodes:
            self.graph.remove_node(node.key)
    def distract_blossom(self, blossom_node: Node):
        self.graph = copy.deepcopy(self.orgGraph)
        node_neigh: Node = self.graph.nodes.get(blossom_node.match.key)
        for neigh in node_neigh.edges:
            if neigh in self.cycle:








