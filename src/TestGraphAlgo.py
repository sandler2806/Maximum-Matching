from unittest import TestCase
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo


class TestGraphAlgo(TestCase):
    def test_get_graph(self):
        best_algo_1 = DiGraph("../data/A1.json")
        best_algo_2 = DiGraph("../data/A2.json")
        best_algo_3 = DiGraph("../data/A3.json")
        best_algo_1_algo = GraphAlgo(best_algo_1)
        best_algo_2_algo = GraphAlgo(best_algo_2)
        best_algo_3_algo = GraphAlgo(best_algo_3)
        self.assertIsNotNone(best_algo_1_algo.get_graph())
        self.assertIsNotNone(best_algo_2_algo.get_graph())
        self.assertIsNotNone(best_algo_3_algo.get_graph())

    def test_load_from_json(self):
        g_algo = GraphAlgo()
        self.assertTrue(g_algo.load_from_json("../data/A1.json"))
        self.assertTrue(g_algo.load_from_json("../data/A2.json"))
        self.assertTrue(g_algo.load_from_json("../data/A3.json"))
        self.assertTrue(g_algo.load_from_json("../data/A4.json"))

    def test_save_to_json(self):
        g_algo = GraphAlgo()
        g_algo.load_from_json("../data/A1.json")
        g_algo.graph.add_node(17, (35.62364, 34.346164, 0))
        g_algo.graph.add_node(14, (32.62364, 33.346164, 0))
        g_algo.graph.add_edge(14, 17, 4.1251)
        self.assertEqual(True, g_algo.save_to_json("../data/b1.json"))
        self.assertEqual(17, g_algo.graph.nodes.get(17).key)
        g_algo2 = GraphAlgo()
        g_algo2.load_from_json("../data/b1.json")
        self.assertEqual(17, g_algo2.graph.nodes.get(17).key)

    def test_center_point(self):
        best_algo_1 = DiGraph("../data/G1.json")
        best_algo_2 = DiGraph("../data/G2.json")
        best_algo_3 = DiGraph("../data/G3.json")
        best_algo_5 = DiGraph("../data/1000Nodes.json")
        best_algo_1_algo = GraphAlgo(best_algo_1)
        best_algo_2_algo = GraphAlgo(best_algo_2)
        best_algo_3_algo = GraphAlgo(best_algo_3)
        best_algo_5_algo = GraphAlgo(best_algo_5)
        self.assertEqual(8, best_algo_1_algo.centerPoint()[0])
        self.assertEqual(0, best_algo_2_algo.centerPoint()[0])
        self.assertEqual(40, best_algo_3_algo.centerPoint()[0])
        self.assertEqual(362, best_algo_5_algo.centerPoint()[0])

    def test_shortest_path(self):
        best_algo_1 = DiGraph("../data/A1.json")
        best_algo_2 = DiGraph("../data/A2.json")
        best_algo_3 = DiGraph("../data/A3.json")
        best_algo_1_algo = GraphAlgo(best_algo_1)
        best_algo_2_algo = GraphAlgo(best_algo_2)
        best_algo_3_algo = GraphAlgo(best_algo_3)
        self.assertEqual((9.52340017845811, [1, 0, 16, 15, 14, 13, 12]), best_algo_1_algo.shortest_path(1, 12))
        self.assertEqual((7.829003890741554, [1, 26, 8, 9, 10, 11, 20]), best_algo_2_algo.shortest_path(1, 20))
        self.assertEqual((0.8676293017022988, [17, 39]), best_algo_3_algo.shortest_path(17, 39))
        g = DiGraph()
        for n in range(4):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 0, 1.1)
        g.add_edge(1, 2, 1.3)
        g.add_edge(2, 3, 1.1)
        g.add_edge(1, 3, 1.9)
        g.remove_edge(1, 3)
        g.add_edge(1, 3, 10)
        g_algo = GraphAlgo(g)
        self.assertEqual((3.4, [0, 1, 2, 3]), g_algo.shortest_path(0, 3))

    def test_tsp(self):
        g = DiGraph()  # creates an empty directed graph
        for n in range(5):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(0, 4, 5)
        g.add_edge(1, 0, 1.1)
        g.add_edge(1, 2, 1.3)
        g.add_edge(1, 3, 1.9)
        g.add_edge(2, 3, 1.1)
        g.add_edge(3, 4, 2.1)
        g.add_edge(4, 2, .5)
        g_algo = GraphAlgo(g)
        self.assertEqual(([1, 2, 3, 4], 4.5), g_algo.TSP([1, 2, 4]))
        g2 = DiGraph("../data/A0.json")
        g_algo.graph = g2
        self.assertEqual(([10, 0, 1, 2, 3, 4], 6.914963541041983), g_algo.TSP([1, 2, 4, 10]))
        g3 = DiGraph("../data/A1.json")
        g_algo.graph = g3
        self.assertEqual(([10, 9, 8, 7, 6, 5, 6, 2, 1, 0], 14.947567898812181), g_algo.TSP([0, 5, 7, 9, 10]))
        self.assertIsNone(g_algo.TSP([0, 5, 7, 9, 100]))

    def test_plot_graph(self):
        best_algo_1 = DiGraph("../data/A1.json")
        best_algo_2 = DiGraph("../data/A2.json")
        best_algo_3 = DiGraph("../data/A3.json")
        best_algo_1_algo = GraphAlgo(best_algo_1)
        best_algo_2_algo = GraphAlgo(best_algo_2)
        best_algo_3_algo = GraphAlgo(best_algo_3)
        self.assertIsNone(best_algo_1_algo.plot_graph())
        self.assertIsNone(best_algo_2_algo.plot_graph())
        self.assertIsNone(best_algo_3_algo.plot_graph())
