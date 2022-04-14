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
    # iterate over the parents until the parent is null and the last parent that is not null is the ancestor.
    while node.parent is not None:
        node = node.parent
        ancestor_lst.append(node)
    return ancestor_lst


def find_cycles(node, node_curr) -> list:
    # find the path to the ancestor for each node
    ans1 = find_ancestor(node)
    ans2 = find_ancestor(node_curr)
    index_ans1 = len(ans1) - 1
    index_ans2 = len(ans2) - 1
    # iterate over the paths until the node is different in order to prevent the same node to appear twice in the cycle.
    while ans1[index_ans1] == ans2[index_ans2]:
        index_ans1 -= 1
        index_ans2 -= 1
    # combine the two different lists to one list and return it.
    return ans1[:index_ans1 + 1] + ans2[index_ans2 + 1::-1]


class MaximumMatching:

    def __init__(self, graph: Graph):
        self.orgGraph = graph
        self.graph = graph
        self.exposed = []
        self.blossoms = []

    def remove_edges_nodes_blossom(self, blossom, cycle):
        for node1, node2 in blossom.org_edges:  # iterate over the original edges of the graph with the blossom nodes
            self.graph.remove_edge(node1.key, node2.key)  # and remove them.
        for node in cycle:  # remove all the nodes from the graph, because they are contained in the blossom.
            self.graph.remove_node(node.key)

    def constract_blossom(self, blossom_nodes: list) -> Node:
        blossom = Node()  # create the blossom node and add it to the graph.
        self.graph.add_node(blossom.key, blossom_nodes[0].geolocation)
        blossom = self.graph.nodes.get(blossom.key)
        blossom.blossom = True
        for node in blossom_nodes:
            blossom.org_nodes.append(node)  # add every node in the cycle to the blossom nodes.
            for edge in node.edges:
                temp_node: Node = self.orgGraph.nodes.get(edge)
                if temp_node not in blossom_nodes:
                    blossom.org_edges.append((node, temp_node))
                    # find for every node in the blossom his edges in the graph that not in the blossom.
                    if temp_node.key not in blossom.edges:
                        self.graph.add_edge(blossom.key, temp_node.key)
                    # if the parent of the node is now in the blossom nodes,
                    # then make the blossom his parent instead his original parent.
                    if temp_node.parent in blossom_nodes:
                        temp_node.parent = blossom
        node_cycle = blossom_nodes[0]
        # iterate over the cycle node until finding the parent that is not in the cycle.
        while node_cycle.parent in blossom_nodes:
            node_cycle = node_cycle.parent
        # set this node match as the match for the blossom ans the node parent as well.
        blossom.parent = node_cycle.parent
        blossom.match = node_cycle.match
        # remove the edges and nodes that now are inside the blossom.
        self.remove_edges_nodes_blossom(blossom, blossom_nodes)
        self.blossoms.insert(0, blossom.key)
        return blossom

    def build_edges(self, blossom: Node):
        # iterate over the blossom nodes and add them to the graph.
        for node in blossom.org_nodes:
            self.graph.add_node(node.key, node.geolocation)
        # build the original edges to the graph.
        for node1, node2 in blossom.org_edges:
            self.graph.add_edge(node1.key, node2.key)
        # add the edges to the new node that has been added.
        for node in blossom.org_nodes:
            for edge in node.edges:
                self.graph.add_edge(node.key, edge)

    def build_edges_new_path(self, blossom):
        # in order to set the match for non incident edges then i want to add match only when the second node has
        # odd index in the cycle.
        for node_index in range(1, len(blossom.org_nodes) - 1):
            if (node_index + 1) % 2 == 0:
                node1 = self.graph.nodes.get(blossom.org_nodes[node_index].key)
                node2 = self.graph.nodes.get(blossom.org_nodes[node_index + 1].key)
                node1.match = node2
                node2.match = node1
        # remove the edges that were connected to the blossom
        for edge in blossom.edges.copy():
            self.graph.remove_edge(edge, blossom.key)

    def distract_blossom(self, blossom_node: Node):
        # build the edges of the nodes that in the blossom.
        self.build_edges(blossom_node)
        # check that the blossom has match
        if blossom_node.match is None:
            node_popped = blossom_node.org_nodes.pop(0)
        else:
            real_node: Node
            real_node = None
            node_neigh: Node = self.graph.nodes.get(blossom_node.match.key)
            # search in the blossom nodes for the node that was connected to the node that has been set has the match
            # for the blossom and set him as the match for the node that was the blossom match.
            for neigh in node_neigh.edges:
                node = self.graph.nodes.get(neigh)
                for contained_node in blossom_node.org_nodes:
                    if neigh == contained_node.key:
                        node_neigh.match = node
                        node.match = node_neigh
                        real_node = node
                        break
            if real_node is not None:
                return
            node_popped = blossom_node.org_nodes.pop(0)
            # pop and append the nodes in the blossom node until the first node is the node that as been set as the
            # match to the node that was the blossom match.
            while node_popped.key != real_node.key:
                blossom_node.org_nodes.append(node_popped)
                node_popped = blossom_node.org_nodes.pop(0)
        blossom_node.org_nodes.insert(0, node_popped)
        # correctly switch the matching and add edges.
        self.build_edges_new_path(blossom_node)
        # remove the blossom node from the graph.
        self.graph.remove_node(blossom_node.key)
        # remove the blossom node from the blossom list.
        self.blossoms.remove(blossom_node.key)

    def findMatching(self):
        augmentingPathFound = True
        self.findExposed()
        while augmentingPathFound and len(self.exposed) > 1:
            augmentingPathFound = False
            for node in self.exposed:
                self.resetNodes()
                path = self.findAugmentingPath(node)
                if len(path) > 0:
                    augmentingPathFound = True
                    alternatePath(path)
                    for blossom in self.blossoms.copy():
                        self.distract_blossom(graph.nodes[blossom])
                    break
            self.findExposed()
        for blossom in self.blossoms.copy():
            self.distract_blossom(graph.nodes[blossom])

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
                        if len(cycle) % 2 == 1 and len(cycle) < graph.v_size():
                            blossom = self.constract_blossom(cycle)
                            for n in cycle:
                                if n in queue:
                                    queue.remove(n)
                            queue.insert(0, blossom)
                            break
                    else:
                        nei.parent = currNode
                        if nei in self.exposed:
                            return createPath(nei)
                        queue.append(nei)
            else:
                nei = currNode.match
                if nei.visited is False:
                    nei.parent = currNode
                    if nei in self.exposed:
                        return createPath(nei)
                else:
                    cycle = find_cycles(nei, currNode)
                    if len(cycle) % 2 == 1:
                        blossom = self.constract_blossom(cycle)
                        for n in cycle:
                            if n in queue:
                                queue.remove(n)
                        queue.insert(0, blossom)
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


if __name__ == '__main__':
    graph = Graph("../data/A5.json")
    mm = MaximumMatching(graph)
    mm.graph.graph_plot()
    mm.findMatching()
    # print()
    mm.graph.graph_plot()
    print(len(mm.exposed))
