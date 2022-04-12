class Node:

    def __init__(self, key: int, geolocation: tuple = (0, 0, 0)):
        self.key = key
        self.geolocation = geolocation
        self.tag = 0
        self.edges = []
        self.parent: Node
        self.parent = None
        self.match: Node
        self.match = None
        self.visited = False

    # add edge
    def add_edge(self, dest: int):
        self.edges.append(dest)

    def clear_node(self):
        self.key = -1
        self.match = None
        self.parent = None
        self.edges.clear()
