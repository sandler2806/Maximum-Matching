class Node:
    max_key = 0

    def __init__(self, key: int = None, geolocation: tuple = (0, 0, 0),org_nodes=[],outer_edges=[]):
        if key is not None:
            if Node.max_key < key:
                Node.max_key = key
            self.key = key
        else:
            self.key = Node.max_key
        Node.max_key += 1
        self.geolocation = geolocation
        self.tag = 0
        self.edges ={3}
        self.edges.clear()
        self.parent: Node
        self.parent = None
        self.match: Node
        self.match = None
        self.visited = False
        self.org_nodes = org_nodes
        self.outer_edges = outer_edges
        self.blossom=False

    # add edge
    def add_edge(self, dest: int):
        self.edges.append(dest)

    def clear_node(self):
        self.match = None
        self.parent = None
        self.edges.clear()
