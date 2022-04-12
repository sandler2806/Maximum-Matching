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


class Blossom(Node):

    def __init__(self):
        Node.__init__(self)
        self.nodes = []
        self.edges = []


class MaximumMatching:

    def __init__(self, graph: Graph):
        self.orgGraph = graph
        self.graph = graph
        self.cycle: List[Node] = []
        self.exposed = []
        self.blossoms = []

    def constract_blossom(self, blossom_nodes: list) -> Node:
        self.cycle = copy.deepcopy(blossom_nodes)
        blossom: Node = copy.deepcopy(blossom_nodes[0])
        blossom.clear_node()
        self.graph.add_node(-1, blossom.geolocation)
        blossom = self.graph.nodes.get(-1)
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
        return blossom

    def build_edges(self):
        for node in self.cycle:
            self.graph.add_node(node.key, node.geolocation)
        for node in self.cycle:
            for edge in node.edges:
                self.graph.add_edge(node.key, edge)

    def distract_blossom(self, blossom_node: Node):
        # self.graph = copy.deepcopy(self.orgGraph)
        self.build_edges()
        real_node: Node
        real_node = None
        node_neigh: Node = self.graph.nodes.get(blossom_node.match.key)
        for neigh in node_neigh.edges:
            node = self.graph.nodes.get(neigh)
            if node in self.cycle:
                node_neigh.match = node
                node.match = node_neigh
                real_node = node
                break
        if real_node is None:
            return
        node_popped = self.cycle.pop(0)
        while node_popped != real_node:
            self.cycle.append(node_popped)
            node_popped = self.cycle.pop(0)
        self.cycle.insert(0, node_popped)
        for node_index in range(1, len(self.cycle) - 1):
            if (node_index + 1) % 2 == 0:
                node1 = self.graph.nodes.get(self.cycle[node_index].key)
                node2 = self.graph.nodes.get(self.cycle[node_index + 1].key)
                node1.match = node2
                node2.match = node1
        self.graph.remove_node(blossom_node.key)

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
        queue: list[Node] = [src]
        while len(queue) != 0:
            currNode = queue.pop(0)
            currNode.visited = True
            if currNode.parent is None or currNode.parent.match == currNode:
                for neiId in currNode.edges:
                    nei = self.graph.nodes.get(neiId)

                    if currNode.parent == nei:
                        continue
                    if nei.visited is True:
                        cycle = find_cycles(nei, currNode)
                        if len(cycle) % 2 == 1:
                            blossom = self.constract_blossom(cycle)
                            for n in cycle:
                                queue.remove(n)
                    nei.parent = currNode

                    if nei in self.exposed:
                        return createPath(nei)
                    queue.append(nei)
            else:
                nei = currNode.match
                nei.parent = currNode
                if nei.visited is False:
                    if nei in self.exposed:
                        return createPath(nei)
                queue.append(nei)

    def findExposed(self):
        for node in self.graph.nodes.values():
            if node.match is None:
                self.exposed.append(node)

    def resetNodes(self):
        for node in self.graph.nodes.values():
            node.parent = None
            node.visited = None
            # self.findExposed()
