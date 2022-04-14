from Graph import Graph
from Node import Node


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


def find_ancestor(node) -> list:
    ancestor_lst = [node]
    while node.parent is not None:
        node = node.parent
        ancestor_lst.append(node)
    return ancestor_lst


def find_cycles(node, node_curr) -> list:
    ans1 = find_ancestor(node)
    ans2 = find_ancestor(node_curr)
    index_ans1 = len(ans1) - 1
    index_ans2 = len(ans2) - 1
    while ans1[index_ans1] == ans2[index_ans2]:
        index_ans1 -= 1
        index_ans2 -= 1
    return ans1[:index_ans1 + 1] + ans2[index_ans2 + 1::-1]


class MaximumMatching:

    def __init__(self, graph: Graph):
        self.orgGraph = graph
        self.graph = graph
        self.exposed = []
        self.blossoms = []

    def construct_blossom(self, blossom_nodes: list) -> Node:
        blossom = Node()
        self.graph.add_node(blossom.key, blossom_nodes[0].geolocation)
        blossom = self.graph.nodes.get(blossom.key)
        blossom.blossom = True
        for node in blossom_nodes:
            blossom.org_nodes.append(node)
            for edge in node.edges:
                temp_node: Node = self.orgGraph.nodes.get(edge)
                if temp_node not in blossom_nodes:
                    blossom.org_edges.append((node, temp_node))
                    if temp_node.key not in blossom.edges:
                        self.graph.add_edge(blossom.key, temp_node.key)
                    if temp_node.parent in blossom_nodes:
                        temp_node.parent = blossom
        node_cycle = blossom_nodes[0]
        while node_cycle.parent in blossom_nodes:
            node_cycle = node_cycle.parent
        blossom.parent = node_cycle.parent
        blossom.match = node_cycle.match
        for node1, node2 in blossom.org_edges:
            self.graph.remove_edge(node1.key, node2.key)
        for node in blossom_nodes:
            self.graph.remove_node(node.key)
        self.blossoms.insert(0, blossom.key)
        return blossom

    def build_edges(self, blossom: Node):
        for node in blossom.org_nodes:
            self.graph.add_node(node.key, node.geolocation,node.org_nodes,node.org_edges)
        for node1, node2 in blossom.org_edges:
            self.graph.add_edge(node1.key, node2.key)
        for node in blossom.org_nodes:
            for edge in node.edges:
                self.graph.add_edge(node.key, edge)

    def distract_blossom(self, blossom_node: Node):
        self.build_edges(blossom_node)

        if blossom_node.match is None:
            node_popped = blossom_node.org_nodes.pop(0)
        else:
            real_node: Node
            real_node = None
            node_neigh: Node = self.graph.nodes.get(blossom_node.match.key)
            for neigh in node_neigh.edges:
                node = self.graph.nodes.get(neigh)
                for c in blossom_node.org_nodes:
                    if neigh == c.key:
                        node_neigh.match = node
                        node.match = node_neigh
                        real_node = node
                        break
            node_popped = blossom_node.org_nodes.pop(0)
            while node_popped.key != real_node.key:
                blossom_node.org_nodes.append(node_popped)
                node_popped = blossom_node.org_nodes.pop(0)
        blossom_node.org_nodes.insert(0, node_popped)
        for node_index in range(1, len(blossom_node.org_nodes) - 1):
            if (node_index + 1) % 2 == 0:
                node1 = self.graph.nodes.get(blossom_node.org_nodes[node_index].key)
                node2 = self.graph.nodes.get(blossom_node.org_nodes[node_index + 1].key)
                node1.match = node2
                node2.match = node1
        for edge in blossom_node.edges.copy():
            self.graph.remove_edge(edge, blossom_node.key)
        self.graph.remove_node(blossom_node.key)
        self.blossoms.remove(blossom_node.key)

    def findMatching(self):
        augmentingPathFound = True
        self.findExposed()
        # we check for augmenting path until no such path exist from each exposed node or if only one exposed node left
        while augmentingPathFound and len(self.exposed) > 1:
            augmentingPathFound = False
            for node in self.exposed:
                self.resetNodes()
                path = self.findAugmentingPath(node)
                # if we found an augmenting path we change the match by alternate the path edges
                if len(path) > 0:
                    augmentingPathFound = True
                    alternatePath(path)
                    # after finding augmenting path we distract all the blossoms
                    for blossom in self.blossoms.copy():
                        self.distract_blossom(graph.nodes.get(blossom))
                    break
            # we update the exposed nodes for the next iteration
            self.findExposed()
        for blossom in self.blossoms.copy():
            self.distract_blossom(graph.nodes.get(blossom))

    """
    This function get a source exposed node and search for augmenting path from it to another exposed node.
    """

    def findAugmentingPath(self, src: Node) -> list:
        queue: list[Node] = [src]
        while len(queue) != 0:
            currNode = queue.pop(0)
            currNode.visited = True
            # if the node is the source or a blossom without a parent or that we came from a edge in the matching
            # so we can go to all the neighbors of the node
            if currNode.parent is None or currNode.parent.match == currNode:
                for neighborId in currNode.edges:

                    neighbor = self.graph.nodes.get(neighborId)
                    # we don't want to go back to the node parent
                    if currNode.parent == neighbor:
                        continue
                    # if the neighbor already visited we found a cycle
                    if neighbor.visited is True:
                        cycle = find_cycles(neighbor, currNode)
                        # if the cycle is odd and doesn't contain all the graph we construct a blossom
                        if len(cycle) % 2 == 1 and len(cycle) < graph.v_size():
                            blossom = self.construct_blossom(cycle)
                            # we remove from the queue all the nodes that in the blossom
                            for n in cycle:
                                if n in queue:
                                    queue.remove(n)
                            queue.insert(0, blossom)
                            break
                    # the neighbor is not visited
                    else:
                        neighbor.parent = currNode
                        if neighbor in self.exposed:
                            return createPath(neighbor)
                        queue.append(neighbor)
            # we can go only to the node that in the match with the currNode
            else:
                neighbor = currNode.match
                if neighbor.visited is False:
                    neighbor.parent = currNode
                    if neighbor in self.exposed:
                        return createPath(neighbor)
                    queue.append(neighbor)
                else:
                    cycle = find_cycles(neighbor, currNode)
                    if len(cycle) % 2 == 1:
                        blossom = self.construct_blossom(cycle)
                        for n in cycle:
                            if n in queue:
                                queue.remove(n)
                        queue.insert(0, blossom)
                        break
        return []

    """
    This function find all the exposed nodes and update the list.
    """
    def findExposed(self):
        self.exposed.clear()
        for node in self.graph.nodes.values():
            if node.match is None:
                self.exposed.append(node)

    """
    This function reset all the node for the next iteration.
    """
    def resetNodes(self):
        for node in self.graph.nodes.values():
            node.parent = None
            node.visited = False


if __name__ == '__main__':
    graph = Graph("../data/A5.json")
    mm = MaximumMatching(graph)
    # mm.graph.graph_plot()
    mm.findMatching()
    mm.graph.graph_plot()
    mm.findExposed()
    print(len(mm.exposed))
