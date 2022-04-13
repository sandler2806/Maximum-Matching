import random
import sys

import pygame

from Node import Node
import json


class Graph:

    def __init__(self, jsonfile: str = None):
        self.nodes: dict[int, Node] = {}
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
                dest = edgeIter['dest']
                if dest not in self.nodes[src].edges:
                    self.add_edge(src, dest)
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

    def all_edges_of_node(self, id1: int) -> dict:
        # if there is no node with the given id in the graph
        if id1 not in self.nodes:
            return []
        return self.nodes[id1].edges

    """return a dictionary of all the nodes connected to (into) node_id ,
                    each node is represented using a pair (other_node_id, weight)
                     """

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

    def add_edge(self, id1: int, id2: int) -> bool:
        node_src = self.nodes.get(id1)
        node_dst = self.nodes.get(id2)
        # if there is no node with one of the given id's or the edge is missing then return false
        if (node_src or node_dst or node_src.outEdges[id2]) is None:
            return False
        else:
            # add the edge to the nodes
            node_src.edges.append(id2)
            node_dst.edges.append(id1)
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
            # edges = self.nodes[node_id].edges.copy()
            # for node_key in edges:
            #     self.remove_edge(node_id, node_key)
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
            if node_id2 in node.edges:
                node.edges.remove(node_id2)
                node2.edges.remove(node_id1)
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

    def graph_plot(self):
        pygame.init()
        scr = pygame.display.set_mode((900, 650))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            scr.fill((255, 255, 255))
            self.set_location()
            scaling = self.caclulate_minmax()
            min_x = scaling[0][0]
            min_y = scaling[0][1]
            lon = scaling[2][0]
            lat = scaling[2][1]
            color = (200, 30, 70)
            font = pygame.font.SysFont('Times ', 12)
            # iterate over the edges first and draw them
            for node in self.nodes:
                for edge in self.all_edges_of_node(node):
                    x1 = (self.nodes[node].geolocation[0] - min_x) * (lon) + 60
                    y1 = (self.nodes[node].geolocation[1] - min_y) * (lat) + 60
                    x2 = (self.nodes[edge].geolocation[0] - min_x) * (lon) + 60
                    y2 = (self.nodes[edge].geolocation[1] - min_y) * (lat) + 60
                    if self.nodes.get(node).match == self.nodes.get(edge):
                        pygame.draw.line(scr, color, (x1, y1), (x2, y2), 2)
                    else:
                        pygame.draw.line(scr, (0, 0, 0), (x1, y1), (x2, y2), 2)

            for node in self.nodes:
                x = (self.nodes[node].geolocation[0] - min_x) * (lon) + 60
                y = (self.nodes[node].geolocation[1] - min_y) * (lat) + 60
                pygame.draw.circle(scr, (0, 0, 0), (x, y), 4)
                txt = font.render(str(node), 1, (0, 150, 255))
                scr.blit(txt, (x - 8, y - 19))

            pygame.display.flip()
        pygame.quit()
