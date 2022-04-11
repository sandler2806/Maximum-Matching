import copy
import json
import math
import sys

import pygame
from abc import ABC
from math import inf
from queue import Queue
from typing import List

# import HelperAlgo
import MinHeapDijkstra
from DiGraph import DiGraph
from GraphAlgoInterface import GraphAlgoInterface
from Node import Node
from src.GraphInterface import GraphInterface


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, graph: DiGraph = None):
        self.graph = graph
        self.g=None
        self.initiated=False

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        # send the file name to the DiGraph in order to use the load function
        self.graph = DiGraph(file_name)
        if self.graph is not None:
            return True
        else:
            return False

    """
    We save to json using the json.dump method
    in order to reach the correct format inorder to dump to json we create a dict which holds 2 keys
    those 2 keys hold lists of nodes and edges which hold dict's of nodes and edges. We add to those
    dict's by iterating over the nodes and edges of the graph and add them
    """

    def save_to_json(self, file_name: str) -> bool:
        nodes_array = []
        edges_array = []
        dictionary = {}
        for i in self.graph.nodes.keys():
            # iterate over the nodes in the graph and for every node insert its info to the list
            node_temp = self.graph.nodes.get(i)
            node_temp: Node
            nodes_dict = {}
            str_pos = node_temp.geolocation.__str__()
            # reformat the geolocation tuple to the json style
            str_pos = str_pos.replace(" ", "")
            str_pos = str_pos.replace("(", "")
            str_pos = str_pos.replace(")", "")
            nodes_dict["pos"] = str_pos
            # insert the id of the node as the id in the list
            nodes_dict["id"] = i
            nodes_array.append(nodes_dict)
            # iterate over the out edges of every node and insert their data to the list
            for j in node_temp.outEdges.keys():
                edge_dict = {}
                w = node_temp.outEdges.get(j)
                edge_dict["src"] = i
                edge_dict["w"] = w
                edge_dict["dest"] = j
                edges_array.append(edge_dict)
        dictionary["Edges"] = edges_array
        dictionary["Nodes"] = nodes_array
        try:
            # dumps the dict to json
            with open(file_name, 'w') as f:
                json.dump(dictionary, f)
                f.close()
            return True
        except:
            return False

    """
    This function returns the shortest between two nodes.
    It return the weight of the path and the shortest path itself. 
    """

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        list_of_path = []
        if(not self.initiated):
            g_algo = GraphAlgo(self.graph)
            # init the dijkstra class
            self.g=MinHeapDijkstra.DijkstraUsingMinHeap.Graph(g_algo)
            self.initiated=True
        try:
            # send the node to the dijkstra function
            self.g.dijkstra_Getmin_distances(id1)
            # if there is no path between the two nodes then raise exception
            if self.g.heap_nodes[id2] == sys.maxsize:
                raise Exception()
            index = id2
            # iterate over the parents list till we reach the starting node
            while index != id1:
                # add the parent to the list
                list_of_path.insert(0, index)
                index = self.g.parents[index]
            # insert the starting node to the start of the path 
            list_of_path.insert(0, id1)
            # save the ans as the tuple contains the dist and the path
            ans = (self.g.heap_nodes[id2], list_of_path)
            return ans
        except:
            return inf, []

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        actual_nodes_lst = []
        # we want to work with a list of nodes rather then a list of the id's of nodes
        for i in node_lst:
            actual_nodes_lst.append(self.graph.nodes.get(i))
        # first we search by a helper function if we even have a path between our node_lst if not we
        # obviously return none
        if not self.find_path(actual_nodes_lst, self.graph):
            return None
        try:
            best_path = []
            min_path = sys.maxsize
            # we will iterate over our node_lst and greedily search whats the best path to take from that node for which
            # we are iterating over ot reach all nodes in out nodes_lst.
            for j in range(len(actual_nodes_lst)):
                hold_cities = list(actual_nodes_lst)
                current = 0
                path = []
                src_i = j
                dest_i, current_dest = 0, 0
                src = actual_nodes_lst[src_i].key
                hold_cities.pop(src_i)
                path.append(src)
                ans: float
                while hold_cities:
                    min_dist = sys.maxsize
                    for i in range(len(hold_cities)):
                        a: int
                        a = hold_cities[i].key
                        ans = 0
                        # if the node we are searching for a path to from our src node is not in the path
                        # already we find the shortest path to it
                        if a not in path:
                            b = self.shortest_path(src, a)
                            ans = b[0]
                        dist = ans
                        # if we found a shorter distance we update that distance and
                        # the nodes we traveled to be the minimum
                        if dist != inf:
                            if dist < min_dist:
                                min_dist = dist
                                current_dest = a
                                dest_i = i
                        else:
                            break
                    current += min_dist
                    temp_path = self.shortest_path(src, current_dest)[1]
                    if temp_path is None:
                        return None  # because this means we couldn't find a path connecting all our nodes
                    flag_first = True
                    # iterate over the current founded path and add it to the path
                    for n in temp_path:
                        if flag_first:
                            flag_first = False
                        else:
                            path.append(n)
                    # now the dest became the src
                    hold_cities.pop(dest_i)
                    src = current_dest
                # the path with minimum dist is the best path
                if current < min_path:
                    min_path = current
                    best_path = path
            return best_path, min_path
        except:
            return None

    def centerPoint(self) -> (int, float):
        min_max_value = sys.maxsize
        index = 0
        g_algo = GraphAlgo(self.graph)
        # init the dijkstra algorithm
        g1 = MinHeapDijkstra.DijkstraUsingMinHeap.Graph(g_algo)
        try:
            # iterate over every node for the algorithm
            for i in self.graph.nodes.keys():
                g1.dijkstra_Getmin_distances(i)
                if g1.max == sys.maxsize:
                    raise Exception()
                # asking if the dist from the node with the maximum dist to the current node is the minimum dist
                if g1.max < min_max_value:
                    min_max_value = g1.max
                    index = i
            # the node with the minimum max dist is the center point 
            ans = (index, min_max_value)
            return ans
        except:
            return None,inf

    def plot_graph(self) -> None:
        # call to the 
        self.graph_plot()

    def is_connected(self) -> bool:
        # if bfs on the regular graph returns false
        if not self.bfs(self.graph):
            return False
        try:
            reversed_graph: DiGraph = self.reverse(self.graph)
            # if bfs on the reversed graph is false
            if not self.bfs(reversed_graph):
                return False
            # if both returned true
            return True
        except:
            return False
    
    """
    This function will use the bfs in order to check if the graph is connected
    """
    def bfs(self, graph: DiGraph) -> bool:
        flag = True
        for node in graph.nodes:  # first lets set tag of all nodes to 0 e.g not visited
            graph.nodes.get(node).tag = 0
        # init the bfs queue for the nodes
        queue = Queue(maxsize=len(graph.nodes))
        # get first node and run bfs from it
        for key in graph.nodes.keys():
            if not flag:
                break
            flag = False
            src: Node = graph.nodes.get(key)
            queue.put(key)
            src.tag = 1
        while not queue.empty():
            current_nodes_key = queue.get()
            neighbors = graph.all_out_edges_of_node(current_nodes_key)
            # iterate over the neighbors of the node
            for neighbor_key in neighbors.keys():
                current_neighbor_node: Node = graph.nodes.get(neighbor_key)
                # now the node is visited
                if current_neighbor_node.tag == 0:
                    current_neighbor_node.tag = 1
                    queue.put(neighbor_key)
        # if we find for some node that its tag is 0 e.g hasn't been visited then return false.
        for node in graph.nodes:
            if graph.nodes.get(node).tag == 0:
                return False
        return True
    """
    The function reversing the edges direction and returns the reversed graph
    """
    def reverse(self, graph: DiGraph) -> DiGraph:
        reversed_graph: DiGraph = DiGraph()
        # traverse through each node
        for connected_key in graph.nodes.keys():
            # only if graph doesn't already have the node then add it
            if connected_key not in reversed_graph.nodes:
                src_bfr_reverse: Node = graph.nodes.get(connected_key)
                reversed_graph.nodes[connected_key] = src_bfr_reverse
            neighbors = graph.all_out_edges_of_node(connected_key)
            # traverse through edges coming out of each node
            for neighbor_of_connected_key in neighbors.keys():
                # only if graph doesn't already have the node then add it
                if neighbor_of_connected_key not in reversed_graph.nodes.keys():  
                    dst_bfr_reverse: Node = graph.nodes.get(neighbor_of_connected_key)
                    reversed_graph.nodes[neighbor_of_connected_key] = dst_bfr_reverse
                weight_of_reversed_edge = graph.nodes.get(neighbor_of_connected_key).inEdges.get(connected_key)
                # add the edge to the new graph
                reversed_graph.add_edge(neighbor_of_connected_key, connected_key, weight_of_reversed_edge)
        return reversed_graph

    """
    @:param nodes -> a list of the tsp nodes we wish to find the shortest path to that visits all of them
    @:param graph ->the graph we are working on 
    @:return bool -> True if there is a path in the graph between all nodes and False otherwise 
    """

    def find_path(self, nodes: List[Node], graph: DiGraph) -> bool:
        copy_graph = GraphAlgo(copy.deepcopy(graph))  # creating a copy of our graph so we dont change the orignal one
        flag1 = True
        try:
            keys = []
            for node_iter in graph.nodes:
                keys.append(node_iter)
            src_node = False
            src_node_key = 0
            for node_iter2 in copy_graph.graph.nodes:
                if not flag1:
                    break
                # greedily search find the node we start from
                if copy_graph.graph.nodes[node_iter2] in nodes:
                    src_node_key = node_iter2
                    src_node = True
                flag1 = False
            if src_node:
                # running the is connected method in order to a check if the graph is connected and b to change the
                # tags on the node according to the dfs traversal through the graph
                copy_graph.is_connected()
                flag1 = True
                for i in keys:
                    if (i != src_node_key) and (graph.nodes.get(i).tag != 1) and (i in keys):
                        return False
            copy_graph.is_connected()
            for i in range(len(keys)):
                key_current = keys[i]
                if (key_current != src_node_key) and (key_current in nodes) and (graph.nodes.get(key_current).tag != 1):
                    return False

            return True
        except:
            return False

    def graph_plot(self, ):
        pygame.init()
        scr = pygame.display.set_mode((900, 650))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            scr.fill((255, 255, 255))
            self.graph.set_location()
            scaling = self.graph.caclulate_minmax()
            min_x = scaling[0][0]
            min_y = scaling[0][1]
            lon = scaling[2][0]
            lat = scaling[2][1]
            color = (200, 30, 70)
            font = pygame.font.SysFont('Times ', 12)
            # iterate over the edges first and draw them
            for node in self.graph.nodes:
                for edge in self.graph.all_out_edges_of_node(node):
                    x1 = (self.graph.nodes[node].geolocation[0] - min_x) * (lon) + 60
                    y1 = (self.graph.nodes[node].geolocation[1] - min_y) * (lat) + 60
                    x2 = (self.graph.nodes[edge].geolocation[0] - min_x) * (lon) + 60
                    y2 = (self.graph.nodes[edge].geolocation[1] - min_y) * (lat) + 60
                    pygame.draw.line(scr, color, (x1, y1), (x2, y2), 2)
            # iterate over every edge and draw arrows to it if needed
            for node in self.graph.nodes:
                for edge in self.graph.all_out_edges_of_node(node):
                    x1 = (self.graph.nodes[node].geolocation[0] - min_x) * (lon) + 60
                    y1 = (self.graph.nodes[node].geolocation[1] - min_y) * (lat) + 60
                    x2 = (self.graph.nodes[edge].geolocation[0] - min_x) * (lon) + 60
                    y2 = (self.graph.nodes[edge].geolocation[1] - min_y) * lat + 60
                    self.draw_arrow_lines(scr, x1, y1, x2, y2, 6, 5)
            # iterate over the nodes and draw them
            for node in self.graph.nodes:
                x = (self.graph.nodes[node].geolocation[0] - min_x) * (lon) + 60
                y = (self.graph.nodes[node].geolocation[1] - min_y) * (lat) + 60
                pygame.draw.circle(scr, (0, 0, 0), (x, y), 4)
                txt = font.render(str(node), 1, (0, 150, 255))
                scr.blit(txt, (x - 8, y - 19))

            pygame.display.flip()
        pygame.quit()

    def draw_arrow_lines(self, scr: pygame.Surface, x1, y1, x2, y2, d, h):
        dx = x2 - x1
        dy = y2 - y1
        D = math.sqrt(dx * dx + dy * dy)
        xm = D - 3.5
        xn = xm
        ym = h
        yn = (0 - h)
        sin = dy / D
        cos = dx / D
        x = xm * cos - ym * sin + x1
        ym = xm * sin + ym * cos + y1
        xm = x
        x = xn * cos - yn * sin + x1
        yn = xn * sin + yn * cos + y1
        xn = x
        newX2 = (xm + xn) / 2
        newY2 = (ym + yn) / 2
        dx1 = newX2 - x1
        dy1 = newY2 - y1
        D1 = math.sqrt(dx1 * dx1 + dy1 * dy1)
        xm1 = D1 - d
        xn1 = xm1
        ym1 = h
        yn1 = 0 - h
        sin1 = dy1 / D1
        cos1 = dx1 / D1
        nx = xm1 * cos1 - ym1 * sin1 + x1
        ym1 = xm1 * sin1 + ym1 * cos1 + y1
        xm1 = nx
        nx = xn1 * cos1 - yn1 * sin1 + x1
        yn1 = xn1 * sin1 + yn1 * cos1 + y1
        xn1 = nx
        points = [(newX2, newY2), (xm1, ym1), (xn1, yn1)]
        pygame.draw.polygon(scr, (200, 30, 70), points)
