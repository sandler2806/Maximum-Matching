import time as t

from Graph import Graph
from Node import Node
from GUI import *


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
        self.graph = graph
        self.exposed = []
        self.blossoms = []

    def findMatching(self):
        augmentingPathFound = True
        self.findExposed()
        # we check for augmenting path until no such path exist from each exposed node or if only one exposed node left
        while augmentingPathFound and len(self.exposed) > 1:
            augmentingPathFound = False
            for node in self.exposed:
                # reset parent and visit for all nodes for next bfs
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
            GUI.draw(mm.graph, len(mm.exposed))
            t.sleep(1)
        for blossom in self.blossoms.copy():
            self.distract_blossom(graph.nodes.get(blossom))

    def findAugmentingPath(self, src: Node) -> list:
        queue: list[Node] = [src]
        # until the queue is empty
        while len(queue) != 0:
            currNode = queue.pop(0)
            currNode.visited = True
            # if the node is the source or a blossom without a parent or that we came from a edge in the matching
            # so we can go to all the neighbors of the node
            if currNode.parent is None or currNode.parent.match == currNode:
                for neighborId in currNode.edges:
                    neighbor = self.graph.nodes.get(neighborId)
                    # we don't want to go back to the parent node
                    if neighbor == currNode.parent:
                        continue
                    # if the neighbor already visited or in the queue we found a cycle
                    if neighbor.visited is True or neighbor in queue:
                        cycle = find_cycles(neighbor, currNode)
                        # if the cycle is odd and doesn't contain all the graph we construct a blossom
                        if len(cycle) % 2 == 1 and len(cycle) < graph.v_size():
                            blossom = self.construct_blossom(cycle)
                            # we remove from the queue all the nodes that in the blossom
                            for n in cycle:
                                if n in queue:
                                    queue.remove(n)
                            queue.insert(0,blossom)
                            # we found two expoed nodes (the src and the blossom) so we can construct an augmenting path
                            if blossom.match is None and blossom.parent is not None:
                                return createPath(blossom)
                            break
                    # the neighbor is not visited and not in the queue
                    else:
                        neighbor.parent = currNode
                        if neighbor in self.exposed:
                            return createPath(neighbor)
                        queue.append(neighbor)
            # we can go only to the node that in the match with the currNode
            else:
                neighbor = currNode.match
                if neighbor.visited is True or neighbor in queue:
                    cycle = find_cycles(neighbor, currNode)
                    if len(cycle) % 2 == 1:
                        blossom = self.construct_blossom(cycle)
                        for n in cycle:
                            if n in queue:
                                queue.remove(n)
                        queue.insert(0, blossom)
                        if blossom.match is None and blossom.parent is not None:
                            return createPath(blossom)
                else:
                    neighbor.parent = currNode
                    queue.append(neighbor)

        return []

    def construct_blossom(self, blossom_nodes: list) -> Node:
        blossom = Node()
        # create the blossom node and add it to the graph.
        self.graph.add_node(blossom.key, blossom_nodes[0].geolocation)
        blossom = self.graph.nodes.get(blossom.key)
        blossom.blossom = True
        for node in blossom_nodes:
            blossom.org_nodes.append(node)  # add every node in the cycle to the blossom nodes.
            for edge in node.edges:
                temp_node: Node = self.graph.nodes.get(edge)
                # find for every node in the blossom his edges in the graph that not in the blossom.
                if temp_node not in blossom_nodes:
                    blossom.outer_edges.append((node, temp_node))
                    # connect the blossom with the neighbors of the nodes that in the blossom only once.
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
        if blossom.match is not None:
            node_cycle.match.match = blossom
        # remove the nodes that inside the blossom and the outer edges from the blossom.
        self.remove_edges_nodes_blossom(blossom, blossom_nodes)
        self.blossoms.insert(0, blossom.key)
        GUI.draw(mm.graph, len(mm.exposed))
        t.sleep(1)
        return blossom

    def remove_edges_nodes_blossom(self, blossom, cycle):
        # iterate over the original edges of the graph with the blossom nodes and remove them.
        for node1, node2 in blossom.outer_edges:
            self.graph.remove_edge(node1.key, node2.key)
        # remove all the nodes from the graph, because they are contained in the blossom.
        for node in cycle:
            self.graph.remove_node(node.key)

    def distract_blossom(self, blossom_node: Node):
        # build the edges of the nodes that in the blossom.
        self.build_edges(blossom_node)
        # check that the blossom has match
        if blossom_node.match is None:
            node_popped = blossom_node.org_nodes.pop(0)
        else:
            # find the node that was matching with the blossom's match and start the list from it
            stemsNei: Node
            stemsNei = None
            blossoms_match: Node = self.graph.nodes.get(blossom_node.match.key)
            # search in the blossom nodes for the node that was matched to the node that has been set as the match
            # for the blossom and set him as the match for the node that was the blossom's match.
            for neigh_id in blossoms_match.edges:
                neigh = self.graph.nodes.get(neigh_id)
                for contained_node in blossom_node.org_nodes:
                    if neigh_id == contained_node.key:
                        blossoms_match.match = neigh
                        neigh.match = blossoms_match
                        stemsNei = neigh
                        break
            node_popped = blossom_node.org_nodes.pop(0)
            # pop and append the nodes in the blossom node until the first node is the node that has been set as the
            # match to the node that was the blossom's match.
            while node_popped.key != stemsNei.key:
                blossom_node.org_nodes.append(node_popped)
                node_popped = blossom_node.org_nodes.pop(0)
        blossom_node.org_nodes.insert(0, node_popped)
        # correctly switch the matching and add edges.
        self.build_edges_new_path(blossom_node)
        # remove the blossom node from the graph.
        self.graph.remove_node(blossom_node.key)
        # remove the blossom node from the blossom list.
        self.blossoms.remove(blossom_node.key)
        GUI.draw(mm.graph, len(mm.exposed))
        t.sleep(1)

    def build_edges(self, blossom: Node):
        # iterate over the blossom nodes and add them to the graph.
        for node in blossom.org_nodes:
            self.graph.add_node(node.key, node.geolocation, node.org_nodes, node.outer_edges)
            if node.key in self.blossoms:
                self.graph.nodes.get(node.key).blossom = True

        # build the original edges to the graph.
        for node1, node2 in blossom.outer_edges:
            self.graph.add_edge(node1.key, node2.key)
        # add the inner edges of the blossom.
        for node in blossom.org_nodes:
            for edge in node.edges:
                self.graph.add_edge(node.key, edge)

    def build_edges_new_path(self, blossom):
        # in order to set the match for non incident edges then i want to add match only when the second node has
        # odd index in the cycle.
        for node_index in range(1, len(blossom.org_nodes) - 1, 2):
            node1 = self.graph.nodes.get(blossom.org_nodes[node_index].key)
            node2 = self.graph.nodes.get(blossom.org_nodes[node_index + 1].key)
            node1.match = node2
            node2.match = node1
        # remove the edges that were connected to the blossom
        for edge in blossom.edges.copy():
            self.graph.remove_edge(edge, blossom.key)

    """
    This function get a source exposed node and search for augmenting path from it to another exposed node.
    """

    """
    This function find all the exposed nodes and update the list.
    """

    def findExposed(self):
        self.exposed.clear()
        for node in self.graph.nodes.values():
            if node.match is None or node != node.match.match:
                self.exposed.append(node)

    """
    This function reset all the node for the next iteration.
    """

    def resetNodes(self):
        for node in self.graph.nodes.values():
            node.parent = None
            node.visited = False


def MinimumLineCover():
    g = Graph("../data/A4.json")
    mlc_match = MaximumMatching(g)
    mlc_edges = []
    for node in mlc_match.graph.nodes.values():
        if node.match is None:
            mlc_edges.append((node.key, node.edges[0]))
        else:
            temp_tuple = (node.key, node.match.key)
            reverse_temp_tuple = (node.match.key, node.key)
            if temp_tuple not in mlc_edges and reverse_temp_tuple not in mlc_edges:
                mlc_edges.append(temp_tuple)
    return mlc_edges


if __name__ == '__main__':
    graph = Graph("../data/A3.json")
    print(graph.v_size())
    mm = MaximumMatching(graph)
    GUI.init_GUI()
    mm.findMatching()
    mm.findExposed()
    print(len(mm.exposed))
    while True:
        GUI.draw(mm.graph, len(mm.exposed), True)
        t.sleep(1)
