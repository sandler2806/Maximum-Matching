class Node:

    def __init__(self, key: int, geolocation: tuple = (0, 0, 0)):
        self.key = key
        self.geolocation = geolocation
        self.tag = 0
        self.edges = []

    # add edge
    def add_edge(self,dest: int):
        self.edges.append(dest)
