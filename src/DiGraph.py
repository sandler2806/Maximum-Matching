import random
import sys

from GraphInterface import GraphInterface
from Node import Node
import json


class DiGraph(GraphInterface):

    def __init__(self, jsonfile: str = None):
        self.nodes = {}
        self._numOfEdges = 0
        self._mc = 0
        if jsonfile is not None:
            with open(jsonfile, 'r') as jsonFile:
                json_object = json.load(jsonFile)
                jsonFile.close()
            # read the json at the Edges and Nodes
            edges_json = json_object['Edges']
            nodes_json = json_object['Nodes']
            # first iterate over the Nodes and add them
            for node_iter in nodes_json:
                if 'pos' in node_iter:
                    location = str(node_iter['pos']).split(',')
                    pos_tuple = (float(location[0]), float(location[1]), float(location[2]))
                    self.add_node(node_iter['id'], pos_tuple)
                # if there is no pos to the node then make the location as (0, 0, 0)
                else:
                    pos_tuple = (0, 0, 0)
                    self.add_node(node_iter['id'], pos_tuple)
            # iterate over the edges and add them
            for edgeIter in edges_json:
                src = edgeIter['src']
                weight = edgeIter['w']
                dest = edgeIter['dest']
                self.add_edge(src, dest, weight)
            self.set_location()
        # if the file is None then give randomize locations
        else:
            self.set_location()

    def v_size(self) -> int:
        return len(self.nodes)

    """
            Returns the number of vertices in this graph
            @return: The number of vertices in this graph
            """

    def e_size(self) -> int:
        return self._numOfEdges

    """
            Returns the number of edges in this graph
            @return: The number of edges in this graph
            """

    def get_all_v(self) -> dict:
        return self.nodes

    """return a dictionary of all the nodes in the Graph, each node is represented using a pair
             (node_id, node_data)
            """

    def all_in_edges_of_node(self, id1: int) -> dict:
        # if there is no node with the given id in the graph
        if id1 not in self.nodes:
            return {}
        return self.nodes[id1].inEdges

    """return a dictionary of all the nodes connected to (into) node_id ,
                    each node is represented using a pair (other_node_id, weight)
                     """

    def all_out_edges_of_node(self, id1: int) -> dict:
        # if there is no node with the given id in the graph
        if id1 not in self.nodes:
            return {}
        return self.nodes[id1].outEdges

    """
    return a dictionary of all the nodes connected from node_id , each node is represented using a pair
    (other_node_id, weight)
    """

    def get_mc(self) -> int:
        return self._mc

    """
    Returns the current version of this graph,
    on every change in the graph state - the MC should be increased
    @return: The current version of this graph.
    """

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        node_src = self.nodes.get(id1)
        node_dst = self.nodes.get(id2)
        # if there is no node with one of the given id's or the edge is missing then return false
        if (node_src or node_dst or node_src.outEdges[id2]) is None:
            return False
        else:
            # add the edge to the nodes
            node_src.outEdges[id2] = weight
            node_dst.inEdges[id1] = weight
            self._mc += 1
            self._numOfEdges += 1
            return True

    """
    Adds an edge to the graph.
    @param id1: The start node of the edge
    @param id2: The end node of the edge
    @param weight: The weight of the edge
    @return: True if the edge was added successfully, False o.w.
    Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
    """

    def add_node(self, node_id: int, pos: tuple = (0, 0, 0)) -> bool:
        node_src = self.nodes.get(node_id)
        # check that the node is not in the graph
        if node_src is not None:
            return False
        else:
            # if the node not in the graph then add it
            node_src = Node(node_id, pos)
            self.nodes[node_id] = node_src
            self._mc += 1
            return True

    """
    Adds a node to the graph.
    @param node_id: The node ID
    @param pos: The position of the node
    @return: True if the node was added successfully, False o.w.
    Note: if the node id already exists the node will not be added
    """

    def remove_node(self, node_id: int) -> bool:
        # if the node is not in the graph
        if self.nodes.get(node_id) is None:
            return False
        else:
            # if the node in the graph run over all of the edges that connected to the node and remove them
            out_edges = self.nodes[node_id].outEdges.copy()
            in_edges = self.nodes[node_id].inEdges.copy()
            for node_key in out_edges.keys():
                self.remove_edge(node_id, node_key)
            for node_key in in_edges.keys():
                self.remove_edge(node_key, node_id)
            # then remove the node
            self.nodes.pop(node_id)
            self._mc += 1
            return True

    """
    Removes a node from the graph.
    @param node_id: The node ID
    @return: True if the node was removed successfully, False o.w.
    Note: if the node id does not exists the function will do nothing
    """

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        node = self.nodes.get(node_id1)
        node2 = self.nodes.get(node_id2)
        # if the nodes with the given ids are not in the graph then return False
        if node is None:
            return False
        if node2 is None:
            return False
        else:
            # if the nodes are in the graph then remove the edge between the nodes
            if node_id2 in node.outEdges:
                node.outEdges.pop(node_id2)
                node2.inEdges.pop(node_id1)
                self._mc += 1
                self._numOfEdges -= 1
                return True
            # if there is no edge between the nodes then return False
            else:
                return False

    """
    Removes an edge from the graph.
    @param node_id1: The start node of the edge
    @param node_id2: The end node of the edge
    @return: True if the edge was removed successfully, False o.w.
    Note: If such an edge does not exists the function will do nothing
    """

    def __repr__(self):
        return "Graph: |V|={} , |E|={}".format(len(self.nodes), self._numOfEdges)

    """
    check if there is node has geolocation, 
    if not it randomize a point between current min point and max point 
    """

    def set_location(self):
        dict_min_max = self.caclulate_minmax()[0]
        for i in self.nodes.values():
            if i.geolocation == (0, 0, 0):
                # check if the given min and max values are correct
                if (dict_min_max[0] != sys.maxsize and dict_min_max[1] != sys.maxsize
                        and dict_min_max[2] != -sys.maxsize and dict_min_max[3] != -sys.maxsize):
                    i.geolocation = (random.uniform(dict_min_max[0], dict_min_max[2]),
                                     random.uniform(dict_min_max[1], dict_min_max[3]), 0)
                else:
                    # randomize location between 0 to 9
                    i.geolocation = (random.uniform(0, 9), random.uniform(0, 9), 0)

    """
    calculate the minimum and maximum values of x and y between the all the nodes in order to use them in the set
    location function and in the graph draw
    """
    def caclulate_minmax(self) -> (tuple, tuple, tuple):
        # set the min and the max values
        minx = sys.maxsize
        miny = sys.maxsize
        max_x = (0 - sys.maxsize)
        maxy = (0 - sys.maxsize)
        node_iter = self.get_all_v()
        # run over all the nodes and check for location values to get the min, max y and x
        for node in node_iter:
            if self.nodes[node].geolocation != (0, 0, 0):
                if self.nodes[node].geolocation[0] < minx:
                    minx = self.nodes[node].geolocation[0]
                if self.nodes[node].geolocation[0] > max_x:
                    max_x = self.nodes[node].geolocation[0]
                if self.nodes[node].geolocation[1] < miny:
                    miny = self.nodes[node].geolocation[1]
                if self.nodes[node].geolocation[1] > maxy:
                    maxy = self.nodes[node].geolocation[1]
        # check if there is node with position
        if minx != sys.maxsize and miny != sys.maxsize and max_x != (0 - sys.maxsize) and maxy != (0 - sys.maxsize):
            abs_x = abs(minx - max_x)
            abs_y = abs(miny - maxy)
            scale_lon = ((900 - 100) / abs_x)
            scale_lat = ((650 - 100) / abs_y)
            return (minx, miny, max_x, max_x), (abs_x, abs_y), (scale_lon, scale_lat)
        else:
            return (minx, miny, max_x, max_x), (0, 0), (0, 0)
