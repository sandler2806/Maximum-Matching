from Graph import Graph
from Node import Node
from queue import Queue


class MaximumMatching:

    def __init__(self, graph: Graph):
        self.orgGraph = graph
        self.graph = graph
        self.exposed = []

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
