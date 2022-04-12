from queue import Queue
from typing import List
from Graph import Graph
from Node import Node
import copy


def createPath(node: Node) -> list:
    path = [node]
    while node.parent is not None:
        node = node.parent
        path.append(node)
    path.reverse()
    return path


def alternatePath(path: list[Node]):
    for i in range(0, len(path), 2):
        node = path[i]
        node.match = path[i + 1]
        path[i + 1].match = node


class MaximumMatching:

    def __init__(self, graph: Graph):
        self.orgGraph = graph
        self.graph = graph
        self.cycle: List[Node] = []
        self.exposed = []
        self.blossoms = []

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
                pass

    def findMatching(self):
        self.findExposed()
        augmentingPathFound = True
        while augmentingPathFound:
            augmentingPathFound = False
            for node in self.exposed:
                self.resetNodes()
                path = self.findAugmentingPath(node)
                if len(path) > 0:
                    augmentingPathFound = True
                    alternatePath(path)
                    break

    def findAugmentingPath(self, src: Node) -> list:
        queue: Queue[Node] = Queue()
        queue.put(src)
        while not queue.empty():
            currNode = queue.get()
            currNode.visited = True
            if currNode.parent is None or currNode.parent.match == currNode:
                for neiId in currNode.edges:
                    nei = self.graph.nodes.get(neiId)

                    if currNode.parent == nei or nei.visited is True:
                        continue
                    nei.parent = currNode

                    if nei in self.exposed:
                        return createPath(nei)
                    queue.put(nei)
            else:
                nei = currNode.match
                nei.parent = currNode
                if nei.visited is False:
                    if nei in self.exposed:
                        return createPath(nei)
                queue.put(nei)

    def findExposed(self):
        for node in self.graph.nodes.values():
            if node.match is None:
                self.exposed.append(node)

    def resetNodes(self):
        for node in self.graph.nodes.values():
            node.parent = None
            node.visited = None
