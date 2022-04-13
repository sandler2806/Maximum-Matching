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
        self.org_nodes = []
        self.org_edges = []


class MaximumMatching:

    def __init__(self, graph: Graph):
        self.orgGraph = graph
        self.graph = graph
        self.cycle: List[Node] = []
        self.exposed = []
        self.blossoms = []

    def constract_blossom(self, blossom_nodes: list) -> Node:
        # self.cycle = copy.deepcopy(blossom_nodes)
        # blossom: Node = Node(None, blossom_nodes[0].geolocation)
        # blossom.clear_node()
        #
        # blossom = self.graph.nodes.get(blossom.key)
        super_node = Blossom()
        super_node.geolocation = blossom_nodes[0].geolocation
        self.graph.add_node(super_node.key, super_node.geolocation)
        for node in blossom_nodes:
            super_node.org_nodes.append(node)
            for edge in node.edges:
                temp_node: Node = self.orgGraph.nodes.get(edge)
                if temp_node not in blossom_nodes:
                    super_node.org_edges.append((node, temp_node))
                    if temp_node.key not in super_node.edges:
                        self.graph.add_edge(super_node.key, temp_node.key)
                    if temp_node.parent in blossom_nodes:
                        temp_node.parent = super_node
        node_cycle = blossom_nodes[0]
        while node_cycle in blossom_nodes:
            node_cycle = node_cycle.parent
        super_node.parent = node_cycle.parent
        super_node.match = node_cycle.match
        for node in blossom_nodes:
            self.graph.remove_node(node.key)
        return super_node

    def build_edges(self, blossom: Blossom):
        for node in blossom.org_nodes:
            self.graph.add_node(node.key, node.geolocation)
        for node1, node2 in blossom.org_edges:
            self.graph.add_edge(node1.key, node2.key)

    def distract_blossom(self, blossom_node: Blossom):
        # self.graph = copy.deepcopy(self.orgGraph)
        self.build_edges(blossom_node)
        real_node: Node
        real_node = None
        node_neigh: Node = self.graph.nodes.get(blossom_node.match.key)
        for neigh in node_neigh.edges:
            node = self.graph.nodes.get(neigh)
            if node in blossom_node.org_nodes:
                node_neigh.match = node
                node.match = node_neigh
                real_node = node
                break
        if real_node is None:
            return
        node_popped = blossom_node.org_nodes.pop(0)
        while node_popped != real_node:
            blossom_node.org_nodes.append(node_popped)
            node_popped = blossom_node.org_nodes.pop(0)
        blossom_node.org_nodes.insert(0, node_popped)
        for node_index in range(1, len(blossom_node.org_nodes) - 1):
            if (node_index + 1) % 2 == 0:
                node1 = self.graph.nodes.get(blossom_node.org_nodes[node_index].key)
                node2 = self.graph.nodes.get(blossom_node.org_nodes[node_index + 1].key)
                node1.match = node2
                node2.match = node1
        self.graph.remove_node(blossom_node.key)

    def findMatching(self):
        augmentingPathFound = True
        while augmentingPathFound:
            self.findExposed()
            augmentingPathFound = False
            for node in self.exposed:
                if node.key == 13:
                    print()
                self.resetNodes()
                path = self.findAugmentingPath(node)
                if len(path) > 0:
                    augmentingPathFound = True
                    alternatePath(path)
                    for blossom in self.blossoms:
                        self.distract_blossom(blossom)
                    break
        for blossom in self.blossoms:
            self.distract_blossom(blossom)

    def findAugmentingPath(self, src: Node) -> list:
        queue: list[Node] = [src]
        while len(queue) != 0:
            currNode = queue.pop(0)
            if currNode.key == 14:
                print()
            currNode.visited = True
            if currNode.parent is None or currNode.parent.match == currNode:
                for neiId in currNode.edges:

                    nei = self.graph.nodes.get(neiId)
                    if currNode.parent == nei:
                        continue

                    if nei.visited is True:
                        cycle = self.find_cycles(nei, currNode)
                        if len(cycle) % 2 == 1:
                            blossom = self.constract_blossom(cycle)
                            for n in cycle:
                                if n in queue:
                                    queue.remove(n)
                            queue.append(blossom)
                            break
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
                else:

                    cycle = self.find_cycles(nei, currNode)
                    if len(cycle) % 2 == 1:
                        blossom = self.constract_blossom(cycle)
                        for n in cycle:
                            if n in queue:
                                queue.remove(n)
                        queue.append(blossom)
                        break
                queue.append(nei)
        return []

    def findExposed(self):
        self.exposed.clear()
        for node in self.graph.nodes.values():
            if node.match is None:
                self.exposed.append(node)

    def resetNodes(self):
        for node in self.graph.nodes.values():
            node.parent = None
            node.visited = False
            # self.findExposed()

    def find_ancestor(self, node) -> list:
        ancestor_lst = [node]
        while node.parent is not None:
            node = node.parent
            ancestor_lst.append(node)
        return ancestor_lst

    def find_cycles(self, node, node_curr) -> list:
        ans1 = self.find_ancestor(node)
        ans2 = self.find_ancestor(node_curr)
        index_ans1 = len(ans1) - 1
        index_ans2 = len(ans2) - 1
        while ans1[index_ans1] != ans2[index_ans2]:
            index_ans1 -= 1
            index_ans2 -= 1
        return ans1[:index_ans1 + 1] + ans2[index_ans2 + 1:-1]


if __name__ == '__main__':
    graph = Graph("../data/A0.json")
    mm=MaximumMatching(graph)
    mm.findMatching()
    mm.graph.graph_plot()
    print()