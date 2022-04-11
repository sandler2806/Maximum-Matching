from unittest import TestCase

from DiGraph import DiGraph


class TestDiGraph(TestCase):

    def test_v_size(self):
        graph = DiGraph("../data/A0.json")
        graph1 = DiGraph("../data/A1.json")
        self.assertEqual(11, graph.v_size())
        self.assertEqual(17, graph1.v_size())

    def test_e_size(self):
        graph = DiGraph("../data/A0.json")
        graph1 = DiGraph("../data/A1.json")
        self.assertEqual(22, graph.e_size())
        self.assertEqual(36, graph1.e_size())

    def test_get_all_v(self):
        string_dict = "{0: 0: |edges out| 2 |edges in| 2, 1: 1: |edges out| 2 |edges in| 2, 2: 2:" \
                      " |edges out| 2 |edges in| 2, 3: 3: |edges out| 2 |edges in| 2," \
                      " 4: 4: |edges out| 2 |edges in| 2, 5: 5: |edges out| 2 |edges in| 2," \
                      " 6: 6: |edges out| 2 |edges in| 2, 7: 7: |edges out| 2 |edges in| 2, " \
                      "8: 8: |edges out| 2 |edges in| 2, 9: 9: |edges out| 2 |edges in| 2, " \
                      "10: 10: |edges out| 2 |edges in| 2}"
        graph = DiGraph("../data/A0.json")
        self.assertEqual(string_dict, graph.get_all_v().__str__())

    def test_all_in_edges_of_node(self):
        g = DiGraph()
        for n in range(4):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 0, 1.1)
        g.add_edge(1, 2, 1.3)
        g.add_edge(2, 3, 1.1)
        g.add_edge(1, 3, 1.9)
        g.remove_edge(1, 3)
        g.add_edge(1, 3, 12)
        in_edges = {2: 1.1, 1: 12}
        self.assertEqual(in_edges, g.all_in_edges_of_node(3))

    def test_all_out_edges_of_node(self):
        g = DiGraph()
        for n in range(4):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 0, 1.1)
        g.add_edge(2, 1, 1.3)
        g.add_edge(2, 3, 1.1)
        g.add_edge(3, 1, 1.9)
        g.add_edge(1, 3, 12)
        out_edges = {1: 1.3, 3: 1.1}
        self.assertEqual(out_edges, g.all_out_edges_of_node(2))

    def test_get_mc(self):
        g = DiGraph()
        for n in range(4):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 0, 1.1)
        g.add_edge(2, 1, 1.3)
        g.add_edge(2, 3, 1.1)
        g.add_edge(3, 1, 1.9)
        g.add_edge(1, 3, 12)
        self.assertEqual(10, g.get_mc())
        g.remove_node(0)
        self.assertEqual(13, g.get_mc())

    def test_add_edge(self):
        g = DiGraph()
        for n in range(4):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 0, 1.1)
        g.add_edge(2, 1, 1.3)
        g.add_edge(2, 3, 1.1)
        g.add_edge(3, 1, 1.9)
        g.add_edge(1, 3, 12)
        g.add_edge(0, 3, 20)
        out_edges = {1: 1, 3: 20}
        self.assertEqual(out_edges, g.all_out_edges_of_node(0))
        in_edges = {2: 1.1, 1: 12, 0: 20}
        self.assertEqual(in_edges, g.all_in_edges_of_node(3))

    def test_add_node(self):
        graph = DiGraph("../data/A0.json")
        self.assertEqual(None, graph.nodes.get(27))
        self.assertTrue(graph.add_node(27, (35.16262, 26.2626, 0)))
        self.assertEqual("27: |edges out| {} |edges in| {}", graph.nodes.get(27).__str__())

    def test_remove_node(self):
        graph = DiGraph("../data/A0.json")
        self.assertEqual(
            "0: |edges out| {1: 1.4004465106761335, 10: 1.4620268165085584} |edges in| {1: 1.8884659521433524, "
            "10: 1.1761238717867548}",
            graph.nodes.get(0).__str__())
        self.assertTrue(graph.remove_node(0))
        self.assertIsNone(graph.nodes.get(0))
        self.assertEqual({}, graph.all_out_edges_of_node(0))
        graph1 = DiGraph("../data/A1.json")
        self.assertEqual(
            "2: |edges out| {1: 1.7155926739282625, 3: 1.1435447583365383} |edges in| {1: 1.7646903245689283, 3: 1.0980094622804095}",
            graph.nodes.get(2).__str__())
        self.assertTrue(graph1.remove_node(0))
        self.assertFalse(graph1.remove_node(250))
        # self.assertEqual("{0: 1.3118716362419698, 15: 1.8726071511162605}", graph1.all_in_edges_of_node(16)._str_())
        # self.assertEqual(False, graph1.remove_edge(1, 16))
        # self.assertEqual("{0: 1.3118716362419698, 15: 1.8726071511162605}", graph1.all_in_edges_of_node(16)._str_())

    def test_remove_edge(self):
        graph = DiGraph("../data/A0.json")
        self.assertEqual("{8: 1.4575484853801393, 10: 1.022651770039933}", graph.all_out_edges_of_node(9).__str__())
        self.assertTrue(graph.remove_edge(9, 10))
        self.assertEqual("{8: 1.4575484853801393}", graph.all_out_edges_of_node(9).__str__())
        graph1 = DiGraph("../data/A1.json")
        self.assertEqual(False, graph1.remove_edge(15, 53))
        self.assertEqual("{0: 1.3118716362419698, 15: 1.8726071511162605}", graph1.all_in_edges_of_node(16).__str__())
        self.assertEqual(False, graph1.remove_edge(1, 16))
        self.assertEqual("{0: 1.3118716362419698, 15: 1.8726071511162605}", graph1.all_in_edges_of_node(16).__str__())
