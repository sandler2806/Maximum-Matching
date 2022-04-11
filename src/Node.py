class Node:

    def __init__(self, key: int, geolocation: tuple = (0, 0, 0)):
        self.key = key
        self.weight = 0
        self.geolocation = geolocation
        self.tag = 0
        self.outEdges = {}
        self.inEdges = {}

    # print the node as we want
    def __repr__(self):
        return "{}: |edges out| {} |edges in| {}".format(self.key, len(self.outEdges), len(self.inEdges))

    def __str__(self):
        return "{}: |edges out| {} |edges in| {}".format(self.key, self.outEdges, self.inEdges)

    # add out edge
    def add_out_edge(self, weight: float, dest: int):
        self.outEdges[dest] = weight
        self.outEdges.values()

    # add in edge
    def add_in_edge(self, weight: float, src: int):
        self.inEdges[src] = weight
