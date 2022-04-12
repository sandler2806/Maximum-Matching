from queue import Queue
from typing import List
from Graph import Graph
from Node import Node
import copy


class MaximumMatching:

    def __init__(self, graph: Graph):
        self.orgGraph = graph
        self.graph = graph
        self.cycle: List[Node] = []
        self.exposed = []


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










    def findMatching(self):
        self.findExposed()
        for node in self.exposed:
            self.resetNodes()
            path = self.findAugmentingPath(node)
            if len(path) == 0:
                pass

    def findAugmentingPath(self, src: Node) -> list:
        queue: Queue[Node] = Queue()
        queue.put(src)
        while not queue.empty():
            currNode = queue.get()
            if currNode.parent is None or currNode.parent.match == currNode:
                for neiId in currNode.edges:
                    nei = self.graph.nodes.get(neiId)
                    if currNode.parent == nei:
                        continue
                    nei.parent = currNode

                    if nei in self.exposed:
                        path = [nei]
                        while nei.parent is not None:
                            nei = nei.parent
                            path.append(nei)
                        return path.reverse()

                    if (currNode.match is None and nei.match is not None) or \
                            (currNode.match is not None and nei.match is None):
                        queue.put(nei)
            else:
                pass

    def findExposed(self):
        for node in self.graph.nodes.values():
            if node.match is None:
                self.exposed.append(node)

    def resetNodes(self):
        for node in self.graph.nodes.values():
            node.parent = None
            node.visited = None
            # self.findExposed()
