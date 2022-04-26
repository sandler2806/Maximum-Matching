import sys
import random

from pygame import gfxdraw
import pygame
from pygame import *
import copy
from types import SimpleNamespace

# from MaximumMatching import *
import MaximumMatching as mm



class GUI:
    min_x: float
    min_y: float
    max_x: float
    max_y: float
    screen = display.set_mode((1080, 720), depth=32, flags=RESIZABLE)
    radius = 15
    FONT: font



    @staticmethod
    def init_GUI():
        # init pygame
        WIDTH, HEIGHT = 1080, 720

        pygame.init()

        GUI.screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)


    @staticmethod
    def draw(graph,exposed):
        mouse = pygame.mouse.get_pos()
        scr = GUI.screen
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                # if the mouse is clicked on the
                # button the game is terminated
                if 20 <= mouse[0] <= 20 + 20 and 20 <= mouse[1] <= 720 + 20:
                    sys.exit()

        scr.fill((255, 255, 255))
        pygame.draw.rect(scr, (183, 0, 0), [20, 20, 20, 20])
        smallfont = pygame.font.SysFont('Corbel', 17, bold=True)
        scr.blit(smallfont.render('exposed:', True, (0, 0, 0)), (50, 20))
        scr.blit(smallfont.render(str(exposed), True, (0, 0, 0)), (120, 20))
        GUI.set_location(graph)
        scaling = GUI.caclulate_minmax(graph)
        min_x = scaling[0][0]
        min_y = scaling[0][1]
        lon = scaling[2][0]
        lat = scaling[2][1]
        color = (200, 30, 70)
        font = pygame.font.SysFont('Times ', 12)
        # iterate over the edges first and draw them
        for node in  graph.nodes:
            for edge in  graph.all_edges_of_node(node):
                x1 = ( graph.nodes[node].geolocation[0] - min_x) * (lon) + 60
                y1 = ( graph.nodes[node].geolocation[1] - min_y) * (lat) + 60
                x2 = ( graph.nodes[edge].geolocation[0] - min_x) * (lon) + 60
                y2 = ( graph.nodes[edge].geolocation[1] - min_y) * (lat) + 60
                if  graph.nodes.get(node).match ==  graph.nodes.get(edge):
                    pygame.draw.line(scr, color, (x1, y1), (x2, y2), 4)
                else:
                    pygame.draw.line(scr, (0, 0, 0), (x1, y1), (x2, y2), 2)

        for node in  graph.nodes:
            x = ( graph.nodes[node].geolocation[0] - min_x) * (lon) + 60
            y = ( graph.nodes[node].geolocation[1] - min_y) * (lat) + 60
            pygame.draw.circle(scr, (0, 0, 0), (x, y), 4)
            txt = font.render(str(node), 1, (0, 150, 255))
            scr.blit(txt, (x - 8, y - 19))

        # pygame.display.flip()


        display.update()

    @staticmethod
    def caclulate_minmax(graph) -> (tuple, tuple, tuple):
        # set the min and the max values
        minx = sys.maxsize
        miny = sys.maxsize
        max_x = (0 - sys.maxsize)
        maxy = (0 - sys.maxsize)
        node_iter =  graph.get_all_v()
        # run over all the nodes and check for location values to get the min, max y and x
        for node in node_iter:
            if  graph.nodes[node].geolocation != (0, 0, 0):
                if  graph.nodes[node].geolocation[0] < minx:
                    minx =  graph.nodes[node].geolocation[0]
                if  graph.nodes[node].geolocation[0] > max_x:
                    max_x =  graph.nodes[node].geolocation[0]
                if  graph.nodes[node].geolocation[1] < miny:
                    miny =  graph.nodes[node].geolocation[1]
                if  graph.nodes[node].geolocation[1] > maxy:
                    maxy =  graph.nodes[node].geolocation[1]
        # check if there is node with position
        if minx != sys.maxsize and miny != sys.maxsize and max_x != (0 - sys.maxsize) and maxy != (0 - sys.maxsize):
            abs_x = abs(minx - max_x)
            abs_y = abs(miny - maxy)
            scale_lon = ((900 - 100) / abs_x)
            scale_lat = ((650 - 100) / abs_y)
            return (minx, miny, max_x, max_x), (abs_x, abs_y), (scale_lon, scale_lat)
        else:
            return (minx, miny, max_x, max_x), (0, 0), (0, 0)

    @staticmethod
    def set_location(graph):
        dict_min_max = GUI.caclulate_minmax(graph)[0]
        for i in  graph.nodes.values():
            if i.geolocation == (0, 0, 0):
                # check if the given min and max values are correct
                if (dict_min_max[0] != sys.maxsize and dict_min_max[1] != sys.maxsize
                        and dict_min_max[2] != -sys.maxsize and dict_min_max[3] != -sys.maxsize):
                    i.geolocation = (random.uniform(dict_min_max[0], dict_min_max[2]),
                                     random.uniform(dict_min_max[1], dict_min_max[3]), 0)
                else:
                    # randomize location between 0 to 9
                    i.geolocation = (random.uniform(0, 9), random.uniform(0, 9), 0)
    # @staticmethod
    # def scale(data, min_screen, max_screen, min_data, max_data):
    #     """
    #     get the scaled data with proportions min_data, max_data
    #     relative to min and max screen dimentions
    #     """
    #     return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen
    #
    # # decorate scale with the correct values
    # @staticmethod
    # def my_scale(data, x=False, y=False):
    #     if x:
    #         return GUI.scale(data, 50, GUI.screen.get_width() - 50, GUI.min_x, GUI.max_x)
    #     if y:
    #         return GUI.scale(data, 50, GUI.screen.get_height() - 50, GUI.min_y, GUI.max_y)
